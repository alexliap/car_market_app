# Car Market App [Streamlit](https://carmarketapp.streamlit.app/)

This is an demo application made for the purpose of semester project for ML course in MSc AI (University of Piraeus x NCSR Demokritos).

As the name of the course suggests, the task was to think of any ML application and develop some algorithms to try and tackle the problem.

In my case I chose two problems:

- When someone wants to sell his car, the first think he does to find out the price of other similar cars with his on the market. We tackle this problem by collecting data on car listings and training **regression models** in order to predict their price.

- Every car guy likes to make comparisons between cars, but most of the time those comaprison are not data driven resulting in false cocnlusions. So a feature of recommending similar cars given a model is implemented using **unsupervised clustering**.

## Data Collection

Data collection was performed, in order to get the car listings data and their features, via an API offered by [Auto.dev](https://www.auto.dev/). Two calls were made once a week:

- One to get basic features, like selling price, make, model, milage etc.

- And another to get features of the cars found in the previous call using their **VIN** number. Data at this step inluded more detailed features like horsepower, mpg, engine congiguration, market category etc.

## App Features

### Price Prediction

For the price prediction task we used multiple instances of [BaggingRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingRegressor.html), which can handle missing values, one for each price segment. For base estimator we used [DecisionTreeRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html).

### Recomendation

For the recommendation feature we used the unsupervised clustering algorithm [HDBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html), which can also handle missing data.

## Technical Details

More info about the project can be found in the [Technical Report](https://github.com/alexliap/car_market_app/blob/master/technical_report.pdf).
