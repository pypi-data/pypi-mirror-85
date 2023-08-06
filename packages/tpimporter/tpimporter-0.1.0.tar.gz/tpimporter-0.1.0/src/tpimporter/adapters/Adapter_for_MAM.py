from typing import List, Dict


class Adapter_For_MAM():
    """
    a class used to alter the keys from the TP import so that the data can be used within MAM
    """
    mam_to_importer_dict = {
        "Tnr": "tnr",
        "tnr2": "tnr",
        "d_id": "did",
        "Status_TP": "status",
        "Titelname": "titel_local",
        "Originaltitel": "titel_ov",
        "Lizenzgeber": "lg",
        "FSK": "rating",
        "ESTStart": "est_start",
        "TVODStart": "tvod_start",
        "PVODStart": "premium_vod_start",
        "DVDStart": "dvd_start",
        "Kinostart": "theatrical_start",
        "Quality": "quality",
        "Studio": "studio",
        "OV": "ov",
        "VendorID": "vendor_id",
        "VendorID_iTunes": "vendor_id_itunes",
        "VendorIDAmazon": "vendor_id_amazon",
        "VendorIDGoogle": "vendor_id_google",
        "VendorIDMicrosoft": "vendor_id_microsoft",
        "VendorIDSky": "vendor_id_sky",
        "VendorIDSony": "vendor_id_sony",
        "VendorIDVodafone": "vendor_id_vodafone",
        "VendorIDMaxdome": "vendor_id_maxdome",
        "VendorIDOnDemand": "vendor_id_ondemand",
        "VendorIDVideoload": "vendor_id_videoload",
        # neu anlegen in db
        "VendorIDRakuten": "vendor_id_wuaki",
        "VendorIDHollystar": "vendor_id_hollystar",
        "VendorIDChili": "vendor_id_chili",
        "VendorIDVideociety": "vendor_id_videociety",
        "VendorIDVideobuster": "vendor_id_videobuster",
        "VendorIDTeleclub": "vendor_id_teleclub",
        "VendorIDUPCCablecom": "vendor_id_cablecom",
        "VendorIDMagentaAT": "vendor_id_magenta_at",
        "VendorIDUnitymedia": "vendor_id_unitymedia",
        # -----------------------
        "Prod_jahr": "production_year",
        "Prod_land": "production_country",
        "DE": "country_de",
        "AT": "country_at",
        "CH": "country_ch",
        "EST": "right_est",
        "TVOD": "right_tvod",
        "SVOD": "right_svod",
        "AVOD": "right_avod",
        "Release_Type": "release_origin",
        "ESTEnde": "est_end",
        "TVODEnde": "tvod_end",
        "PVODEnde": "premium_vod_end",
        "Holdback_EST_Start": "holdback_est_start",
        "Holdback_EST_End": "holdback_est_end",
        "Holdback_TVOD_Start": "holdback_tvod_start",
        "Holdback_TVOD_End": "holdback_tvod_end",
        "InitialPriceHD": "pricing_initial_hd_de",
        "InitialPriceSD": "pricing_initial_sd_de",
        "InitialTier_iTunes_HD_DEAT": "pricetier_initial_itunes_est_hd_de",
        "InitialTier_iTunes_SD_DEAT": "pricetier_initial_itunes_est_sd_de",
        "InitialTier_iTunes_HD_CH": "pricetier_initial_itunes_est_hd_ch",
        "InitialTier_iTunes_SD_CH": "pricetier_initial_itunes_est_sd_ch",
        "FirstRepriceTier_Start": "pricing_1streprice_start",
        "FirstRepriceHD": "pricing_1streprice_hd",
        "FirstRepriceSD": "pricing_1streprice_sd",
        "FirstRepriceTier_iTunes_HD_DEAT": "pricetier_1streprice_itunes_est_hd_de",
        "FirstRepriceTier_iTunes_SD_DEAT": "pricetier_1streprice_itunes_est_sd_de",
        "FirstRepriceTier_iTunes_HD_CH": "pricetier_1streprice_itunes_est_hd_ch",
        "FirstRepriceTier_iTunes_SD_CH": "pricetier_1streprice_itunes_est_sd_ch",
        "iTunes_Status": "pf_status_itunes",
        "Amazon_Status": "pf_status_amazon",
        "channel_type": "channel_type",  # muss implementiert werden
        "mandant": "mandant",
    }

    def transform(self, tp_data: List[Dict]) -> List[Dict]:
        """
        transforms the given dictionaries to a form defined in the class variable
        :param tp_data: a list of dictionaries coming from the TP-Importer
        :return: List[Dict] (with adapted keys fitting the specific service)
        """
        tp_data_mam = []
        for title in tp_data:
            title_dict_mam = dict()
            for key_mam, key_tpimporter in self.mam_to_importer_dict.items():
                title_dict_mam[key_mam] = title.get(key_tpimporter)
            tp_data_mam.append(title_dict_mam)
        return tp_data_mam
