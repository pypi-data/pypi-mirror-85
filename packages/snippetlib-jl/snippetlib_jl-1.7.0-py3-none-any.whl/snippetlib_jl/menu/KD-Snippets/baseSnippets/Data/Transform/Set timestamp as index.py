# Set timestamp as index

format = '%Y-%m-%d %H:%M:%S.%f'
data['time'] = pd.to_datetime(data['time'], format=format)
data = data.set_index(['time'])
data = data.sort_index()