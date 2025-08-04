import tkinter as tk
from tkinter import messagebox
from PIL import Image ,ImageTk
import pandas as pd 
import numpy as np
from sklearn.linear_model import LinearRegression 
import joblib 

# Step 1: Create Sample Data
data = {
    'Brand': ['Samsung', 'Apple', 'Xiaomi', 'OnePlus', 'Realme', 'Samsung', 'Apple', 'Xiaomi', 'OnePlus', 'Realme'],
    'RAM_GB': [4, 6, 6, 8, 4, 8, 4, 3, 12, 6],
    'Storage_GB': [64, 128, 64, 128, 64, 128, 256, 32, 256, 128],
    'Battery_mAh': [4000, 3000, 4500, 5000, 4300, 4500, 3500, 4000, 4800, 5000],
    'Camera_MP': [48, 12, 64, 108, 64, 108, 12, 48, 50, 64],
    'Price': [15000, 70000, 13000, 30000, 12000, 25000, 65000, 10000, 35000, 16000]
}
df = pd.DataFrame(data)
df = pd.get_dummies(df, columns=['Brand'], drop_first=True)

# Step 2: Train model
X = df.drop('Price', axis=1)
y = df['Price']
model = LinearRegression()
model.fit(X, y)
joblib.dump(model, 'smartphone_price_model.pkl')

# Step 3: Predict function
def predict_price():
    try:
        ram = int(ram_var.get())
        storage = int(storage_var.get())
        battery = int(battery_var.get())
        camera = int(camera_var.get())
        brand = brand_var.get()

        brand_features = {
            "Brand_OnePlus": 1 if brand == "OnePlus" else 0,
            "Brand_Realme": 1 if brand == "Realme" else 0,
            "Brand_Samsung": 1 if brand == "Samsung" else 0,
            "Brand_Xiaomi": 1 if brand == "Xiaomi" else 0,
        }

        features = [ram, storage, battery, camera] + list(brand_features.values())
        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)[0]
        result_label.config(text=f"💰 Estimated Price: ₹{int(prediction):,}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Step 4: GUI Setup
root = tk.Tk()
root.title("📱 Smartphone Price Estimator")
root.geometry("600x500")

# Load background image
bg_image = Image.open("C:\\Users\\shree\\Downloads\\bgfile.jpg")
bg_image = bg_image.resize((600, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Title
tk.Label(root, text="Smartphone Price Estimator", font=("Helvetica", 18, "bold"),
         fg="#ffffff", bg="#2c3e50", padx=20, pady=10).pack(fill="x")

frame = tk.Frame(root, bg='#ffffff', bd=3, relief="ridge")
frame.place(relx=0.5, rely=0.52, anchor="center")

# Dropdown and Inputs
def create_field(name, var, row):
    tk.Label(frame, text=name + ":", font=('Arial', 11, 'bold'), bg='white').grid(row=row, column=0, sticky="e", pady=5, padx=10)
    entry = tk.Entry(frame, textvariable=var, width=25, font=('Arial', 10))
    entry.grid(row=row, column=1, pady=5, padx=10)
    return entry

brand_var = tk.StringVar()
brand_var.set("Samsung")

tk.Label(frame, text="Brand:", font=('Arial', 11, 'bold'), bg='white').grid(row=0, column=0, sticky="e", pady=5, padx=10)
tk.OptionMenu(frame, brand_var, "Apple", "Samsung", "Xiaomi", "OnePlus", "Realme").grid(row=0, column=1, pady=5, padx=10)

ram_var = tk.StringVar()
storage_var = tk.StringVar()
battery_var = tk.StringVar()
camera_var = tk.StringVar()

create_field("RAM (GB)", ram_var, 1)
create_field("Storage (GB)", storage_var, 2)
create_field("Battery (mAh)", battery_var, 3)
create_field("Camera (MP)", camera_var, 4)

# Predict Button
tk.Button(frame, text="Estimate Price", command=predict_price, bg="#1abc9c", fg="white",
          font=('Arial', 11, 'bold'), padx=10, pady=5, relief="flat").grid(row=5, column=0, columnspan=2, pady=15)

# Result
result_label = tk.Label(root, text="💰 Estimated Price: ₹0", font=('Arial', 14, 'bold'),
                        bg="#34495e", fg="white", pady=10)
result_label.pack(side="bottom", fill="x")

root.mainloop()
