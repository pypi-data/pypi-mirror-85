import os

from sbmlutils.modelcreator import creator


base_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.join(base_dir, "results")


if __name__ == "__main__":
    creator.create_model(
        modules=["sbmlutils.examples.models.dallaman.model"], output_dir=target_dir
    )
