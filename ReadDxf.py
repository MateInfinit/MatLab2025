import ezdxf

# Load the DXF file
dxf_file = "cactus_3d.dxf"  # Replace with your file path
doc = ezdxf.readfile(dxf_file)

# Access the modelspace (where the drawing entities are stored)
msp = doc.modelspace()

# Iterate over entities in the DXF file
for entity in msp:
    print(entity.dxftype(), entity.dxf.layer, entity.dxf.color)
