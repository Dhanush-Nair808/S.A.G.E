print("=== STARTING DIAGNOSTIC ===")
print("This should appear immediately")

import os
print(f"Current folder: {os.getcwd()}")

# Check possible model locations
paths = [
    "ml/models",
    "models",
    r"C:\Users\Dhanush Nair\OneDrive\Desktop\S.A.G.E\backend\ml\models"
]

print("\n=== LOOKING FOR MODELS ===")
for p in paths:
    abs_p = os.path.abspath(p)
    print(f"Checking: {abs_p}")
    if os.path.exists(abs_p):
        print("   ✅ Folder FOUND")
        files = [f for f in os.listdir(abs_p) if f.endswith(".pkl")]
        if files:
            print(f"   📦 Models found: {files}")
        else:
            print("   No .pkl files")
    else:
        print("   ❌ Not found")

print("\n=== DONE ===")