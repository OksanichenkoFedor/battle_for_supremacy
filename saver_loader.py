import os
from zipfile import ZipFile
import shutil
from omegaconf import OmegaConf

class SaverLoader:
    def __init__(self, field):
        self.field = field

    def load(self):
        field_dict = OmegaConf.to_container(OmegaConf.load("field_dict.yaml"))
        self.field.side_size = int(field_dict["side_size"])
        self.field.num_iter = 0
        self.field.color_hex = 0
        self.field.radius = self.field.side_size - 1
        return field_dict

    def save(self):
        hex = str(self.field.num_iter) + "_" + str(self.field.color_hex)
        if "field_dict.yaml" in os.listdir():
            shutil.copy2("field_dict.yaml", "old_field_dict.yaml")
            os.remove("field_dict.yaml")
        field_dict = {
            "side_size": self.field.side_size,
            "hex": hex,
            "id": [],
            "q": [],
            "r": [],
            "size": [],
            "color_id": [],
            "is_team_base": [],
            "is_star": []
        }
        for hexagon in self.field.hexagons:
            field_dict["id"].append(hexagon.id)
            field_dict["q"].append(hexagon.q)
            field_dict["r"].append(hexagon.r)
            field_dict["size"].append(hexagon.size)
            field_dict["color_id"].append(hexagon.color_id)
            field_dict["is_team_base"].append(hexagon.is_team_base)
            field_dict["is_star"].append(hexagon.is_star)
        conf = OmegaConf.create(field_dict)
        OmegaConf.save(config=conf, f="field_dict.yaml")
