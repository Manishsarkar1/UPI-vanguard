from preprocess import preprocess

x, encoders = preprocess("../UPI-vanguard/data/upi_transactions.csv")
print("Shape of preprocessed data:", x.shape)
print("Preprocessing complete. Processed data:")
print(x.head(1000)) # Displaying first 1000 rows of the preprocessed data
