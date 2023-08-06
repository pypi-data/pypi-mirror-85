import ee
import math


def slope_correction(image, elevation, model, buffer=0):
    """This function applies the slope correction on a collection of Sentinel-1 data
    Function based on https://doi.org/10.3390/rs12111867
    Adapted from https://github.com/ESA-PhiLab/radiometric-slope-correction/blob/master/notebooks/1%20-%20Generate%20Data.ipynb
       
       :param collection: ee.Collection of Sentinel-1
       :param elevation: ee.Image of DEM
       :param model: model to be applied (volume/surface)
       :param buffer: buffer in meters for layover/shadow amsk
        
        :returns: ee.Image
    """

    def _volumetric_model_SCF(theta_iRad, alpha_rRad):
        """Code for calculation of volumetric model SCF
        
        :param theta_iRad: ee.Image of incidence angle in radians
        :param alpha_rRad: ee.Image of slope steepness in range
        
        :returns: ee.Image
        """

        # model
        nominator = (ninetyRad.subtract(theta_iRad).add(alpha_rRad)).tan()
        denominator = (ninetyRad.subtract(theta_iRad)).tan()
        return nominator.divide(denominator)

    def _surface_model_SCF(theta_iRad, alpha_rRad, alpha_azRad):
        """Code for calculation of direct model SCF
        
        :param theta_iRad: ee.Image of incidence angle in radians
        :param alpha_rRad: ee.Image of slope steepness in range
        :param alpha_azRad: ee.Image of slope steepness in azimuth
        
        :returns: ee.Image
        """

        # model
        nominator = (ninetyRad.subtract(theta_iRad)).cos()
        denominator = alpha_azRad.cos().multiply(
            (ninetyRad.subtract(theta_iRad).add(alpha_rRad)).cos()
        )

        return nominator.divide(denominator)

    def _erode(image, distance):
        """Buffer function for raster

      :param image: ee.Image that should be buffered
      :param distance: distance of buffer in meters
        
      :returns: ee.Image
      """

        d = (
            image.Not()
            .unmask(1)
            .fastDistanceTransform(30)
            .sqrt()
            .multiply(ee.Image.pixelArea().sqrt())
        )

        return image.updateMask(d.gt(distance))

    def _masking(alpha_rRad, theta_iRad, buffer):
        """Masking of layover and shadow
        
        
        :param alpha_rRad: ee.Image of slope steepness in range
        :param theta_iRad: ee.Image of incidence angle in radians
        :param buffer: buffer in meters
        
        :returns: ee.Image
        """
        # layover, where slope > radar viewing angle
        layover = alpha_rRad.lt(theta_iRad).rename("layover")

        # shadow
        ninetyRad = ee.Image.constant(90).multiply(np.pi / 180)
        shadow = alpha_rRad.gt(
            ee.Image.constant(-1).multiply(ninetyRad.subtract(theta_iRad))
        ).rename("shadow")

        # add buffer to layover and shadow
        if buffer > 0:
            layover = _erode(layover, buffer)
            shadow = _erode(shadow, buffer)

        # combine layover and shadow
        no_data_mask = layover.And(shadow).rename("no_data_mask")

        return layover.addBands(shadow).addBands(no_data_mask)

    def _correct(image):
        """This function applies the slope correction and adds layover and shadow masks
        
        """

        # get the image geometry and projection
        geom = image.geometry()
        proj = image.select(1).projection()

        # calculate the look direction
        heading = (
            ee.Terrain.aspect(image.select("angle"))
            .reduceRegion(ee.Reducer.mean(), geom, 1000)
            .get("aspect")
        )

        # Sigma0 to Power of input image
        sigma0Pow = ee.Image.constant(10).pow(image.divide(10.0))

        # the numbering follows the article chapters
        # 2.1.1 Radar geometry
        theta_iRad = image.select("angle").multiply(np.pi / 180)
        phi_iRad = ee.Image.constant(heading).multiply(np.pi / 180)

        # 2.1.2 Terrain geometry
        alpha_sRad = (
            ee.Terrain.slope(elevation)
            .select("slope")
            .multiply(np.pi / 180)
            .setDefaultProjection(proj)
            .clip(geom)
        )
        phi_sRad = (
            ee.Terrain.aspect(elevation)
            .select("aspect")
            .multiply(np.pi / 180)
            .setDefaultProjection(proj)
            .clip(geom)
        )

        # we get the height, for export
        height = elevation.setDefaultProjection(proj).clip(geom)

        # 2.1.3 Model geometry
        # reduce to 3 angle
        phi_rRad = phi_iRad.subtract(phi_sRad)

        # slope steepness in range (eq. 2)
        alpha_rRad = (alpha_sRad.tan().multiply(phi_rRad.cos())).atan()

        # slope steepness in azimuth (eq 3)
        alpha_azRad = (alpha_sRad.tan().multiply(phi_rRad.sin())).atan()

        # local incidence angle (eq. 4)
        theta_liaRad = (
            alpha_azRad.cos().multiply((theta_iRad.subtract(alpha_rRad)).cos())
        ).acos()
        theta_liaDeg = theta_liaRad.multiply(180 / np.pi)

        # 2.2
        # Gamma_nought
        gamma0 = sigma0Pow.divide(theta_iRad.cos())
        gamma0dB = (
            ee.Image.constant(10)
            .multiply(gamma0.log10())
            .select(["VV", "VH"], ["VV_gamma0", "VH_gamma0"])
        )
        ratio_gamma = (
            gamma0dB.select("VV_gamma0")
            .subtract(gamma0dB.select("VH_gamma0"))
            .rename("ratio_gamma0")
        )

        if model == "volume":
            scf = _volumetric_model_SCF(theta_iRad, alpha_rRad)

        if model == "surface":
            scf = _surface_model_SCF(theta_iRad, alpha_rRad, alpha_azRad)

        # apply model for Gamm0_f
        gamma0_flat = gamma0.divide(scf)
        gamma0_flatDB = (
            ee.Image.constant(10)
            .multiply(gamma0_flat.log10())
            .select(["VV", "VH"], ["VV_gamma0flat", "VH_gamma0flat"])
        )

        masks = _masking(alpha_rRad, theta_iRad, buffer)

        # calculate the ratio for RGB vis
        ratio_flat = (
            gamma0_flatDB.select("VV_gamma0flat")
            .subtract(gamma0_flatDB.select("VH_gamma0flat"))
            .rename("ratio_gamma0flat")
        )

        return (
            image.rename(["VV_sigma0", "VH_sigma0", "incAngle"])
            .addBands(gamma0dB)
            .addBands(ratio_gamma)
            .addBands(gamma0_flatDB)
            .addBands(ratio_flat)
            .addBands(alpha_rRad.rename("alpha_rRad"))
            .addBands(alpha_azRad.rename("alpha_azRad"))
            .addBands(phi_sRad.rename("aspect"))
            .addBands(alpha_sRad.rename("slope"))
            .addBands(theta_iRad.rename("theta_iRad"))
            .addBands(theta_liaRad.rename("theta_liaRad"))
            .addBands(masks)
            .addBands(height.rename("elevation"))
        )

    # create a 90 degree image in radians
    ninetyRad = ee.Image.constant(90).multiply(math.pi / 180)

    # run and return correction
    return _correct(image)


def terrain(img, elevation):

    degree2radian = 0.01745
    thermalBand = img.select(["thermal"])

    def topoCorr_IC(img):

        dem = ee.Image("JAXA/ALOS/AW3D30_V1_1").select("MED")

        # Extract image metadata about solar position
        SZ_rad = (
            ee.Image.constant(ee.Number(img.get("SOLAR_ZENITH_ANGLE")))
            .multiply(degree2radian)
            .clip(img.geometry().buffer(10000))
        )
        SA_rad = (
            ee.Image.constant(ee.Number(img.get("SOLAR_AZIMUTH_ANGLE")))
            .multiply(degree2radian)
            .clip(img.geometry().buffer(10000))
        )

        # Creat terrain layers
        slp = ee.Terrain.slope(dem).clip(img.geometry().buffer(10000))
        slp_rad = (
            ee.Terrain.slope(dem)
            .multiply(degree2radian)
            .clip(img.geometry().buffer(10000))
        )
        asp_rad = (
            ee.Terrain.aspect(dem)
            .multiply(degree2radian)
            .clip(img.geometry().buffer(10000))
        )

        # Calculate the Illumination Condition (IC)
        # slope part of the illumination condition
        cosZ = SZ_rad.cos()
        cosS = slp_rad.cos()
        slope_illumination = cosS.expression(
            "cosZ * cosS", {"cosZ": cosZ, "cosS": cosS.select("slope")}
        )

        # aspect part of the illumination condition
        sinZ = SZ_rad.sin()
        sinS = slp_rad.sin()
        cosAziDiff = (SA_rad.subtract(asp_rad)).cos()
        aspect_illumination = sinZ.expression(
            "sinZ * sinS * cosAziDiff",
            {"sinZ": sinZ, "sinS": sinS, "cosAziDiff": cosAziDiff},
        )

        # full illumination condition (IC)
        ic = slope_illumination.add(aspect_illumination)

        # Add IC to original image
        img_plus_ic = ee.Image(
            img.addBands(ic.rename(["IC"]))
            .addBands(cosZ.rename(["cosZ"]))
            .addBands(cosS.rename(["cosS"]))
            .addBands(slp.rename(["slope"]))
        )

        return ee.Image(img_plus_ic)

    def topoCorr_SCSc(img):
        img_plus_ic = img
        mask1 = img_plus_ic.select("nir").gt(-0.1)
        mask2 = (
            img_plus_ic.select("slope")
            .gte(5)
            .And(img_plus_ic.select("IC").gte(0))
            .And(img_plus_ic.select("nir").gt(-0.1))
        )

        img_plus_ic_mask2 = ee.Image(img_plus_ic.updateMask(mask2))

        bandList = ["blue", "green", "red", "nir", "swir1", "swir2"]
        # Specify Bands to topographically correct

        def applyBands(image):
            blue = apply_SCSccorr("blue").select(["blue"])
            green = apply_SCSccorr("green").select(["green"])
            red = apply_SCSccorr("red").select(["red"])
            nir = apply_SCSccorr("nir").select(["nir"])
            swir1 = apply_SCSccorr("swir1").select(["swir1"])
            swir2 = apply_SCSccorr("swir2").select(["swir2"])
            return replace_bands(image, [blue, green, red, nir, swir1, swir2])

        def apply_SCSccorr(band):
            method = "SCSc"

            out = (
                ee.Image(1)
                .addBands(img_plus_ic_mask2.select("IC", band))
                .reduceRegion(
                    reducer=ee.Reducer.linearRegression(2, 1),
                    geometry=ee.Geometry(img.geometry().buffer(-5000)),
                    scale=900,
                    bestEffort=True,
                    maxPixels=1e10,
                )
            )

            fit = out.combine({"coefficients": ee.Array([[1], [1]])}, False)

            # Get the coefficients as a nested list,
            # cast it to an array, and get just the selected column
            out_a = ee.Array(fit.get("coefficients")).get([0, 0])
            out_b = ee.Array(fit.get("coefficients")).get([1, 0])
            out_c = out_a.divide(out_b)

            # apply the SCSc correction
            SCSc_output = img_plus_ic_mask2.expression(
                "((image * (cosB * cosZ + cvalue)) / (ic + cvalue))",
                {
                    "image": img_plus_ic_mask2.select([band]),
                    "ic": img_plus_ic_mask2.select("IC"),
                    "cosB": img_plus_ic_mask2.select("cosS"),
                    "cosZ": img_plus_ic_mask2.select("cosZ"),
                    "cvalue": out_c,
                },
            )

            return ee.Image(SCSc_output)

        # img_SCSccorr = ee.Image([apply_SCSccorr(band) for band in bandList]).addBands(img_plus_ic.select('IC'));
        img_SCSccorr = (
            applyBands(img).select(bandList).addBands(img_plus_ic.select("IC"))
        )

        bandList_IC = ee.List([bandList, "IC"]).flatten()

        img_SCSccorr = img_SCSccorr.unmask(img_plus_ic.select(bandList_IC)).select(
            bandList
        )

        return img_SCSccorr.unmask(img_plus_ic.select(bandList))

    img = topoCorr_IC(img)
    img = topoCorr_SCSc(img)

    return img.addBands(thermalBand)

