# Machine Learning Models

This folder contains the training scripts and logic for the Machine Learning models used in RentMate.

## Price Prediction Model (`train_price_model.py`)
This script uses `scikit-learn` to train a **Random Forest Regressor** model to predict the optimal rental price for an item based on its category and condition. 

The approach is inspired by the "House Rent Prediction Dataset" mentioned in the abstract, but adapted for peer-to-peer item rentals.
1. We generate a dataset of items with varied conditions and categories.
2. We apply Label Encoding to categorical data.
3. We train a `RandomForestRegressor`.
4. We save the resulting model as a serialized `.pkl` file in the `saved_models` directory.

The Flask backend dynamically loads this `.pkl` file (inside `backend/ai/price_assistant.py`) to provide real-time price suggestions to owners when listing items.

## Semantic AI Matching Engine
The NLP semantic matching engine (using `sentence-transformers`) is implemented as an active service inside the `backend/ai/matcher.py` folder, since it relies heavily on calculating cosine similarities on-the-fly directly against live database items.

To test the ML price training, simply run:
```bash
python train_price_model.py
```
