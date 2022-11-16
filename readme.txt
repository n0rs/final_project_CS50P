EasyStock
Video Demo: https://youtu.be/-spcYKXDTHU
Description:

EasyStock is a program in a file called project.py that calls an API to analyze stock data. This API contains around 12500 stocks and ETFs traded at the US stock exchange.

EasyStock first asks the user for the stock he wants to analyze. This input is checked to be in the list of actively traded stocks of the used API. If it is not the user gets reprompted for a valid stock. If the input is a a valid stock the program continues.

This function is tested in test_project.py by mocking potential input and checking if the function returns it correctly.

After acquiering a valid stock the program asks the user in what time range he wants to analyze the data. There are four frequencies the user can choose from. These frequencies are connected to a dictionary that contains all the frequencies and that contains the string which has to be included in the URL to make a request. This is also tested by mocking the user input and checking if the function returns correctly.

The program then continues to create an API call for the desired stock and frequency. If you chose the frequency "intraday" it then asks the user to further specify the interval in which the data points should be taken(in minutes). If this again turns out to be a valid interval it goes ahead and makes a request to the API returning a csv-styled data set. If the request fails the program continues.

This function is tested using mock to mock the input of the interval if "intraday"-data was requested. It then asserts that the status code of the request is 200. This tests that there was no failure in the request.

Once the API request went through EasyStock decodes its contents and writes the data into a csv file with the name of the stock and the frequency to ensure no data is overwritten with different frequencies or even stocks. The csv then contains the data with the oldest data point at the top and the newest at the bottom.

After that the program plots the data using matplotlib. On the X-axis the time will be shown while on the Y-axis the price of the stock in USD will be shown. Since VSCode doesnt interact with matplotlip.show i chose to save the plot as a PNG-file in the directory the program is used in.