import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv('/Users/sarahpeng/Desktop/Airports2.csv')
print(df.head(10))


# Ensure the 'Fly_date' column is in the correct format, and filter for 2009
df['Fly_date'] = pd.to_datetime(df['Fly_date'], format='%Y-%m-%d')
df_2009 = df[df['Fly_date'].dt.year == 2009]

# Group by both Origin_airport and Destination_airport to get total flights at each airport
origin_traffic = df_2009.groupby('Origin_airport')['Flights'].sum().reset_index()
origin_traffic.columns = ['Airport', 'Flights_from']
destination_traffic = df_2009.groupby('Destination_airport')['Flights'].sum().reset_index()
destination_traffic.columns = ['Airport', 'Flights_to']

# Merge the data to get total traffic for each airport
airport_traffic = pd.merge(origin_traffic, destination_traffic, on='Airport', how='outer').fillna(0)
# Calculate total traffic (flights coming and going)
airport_traffic['Total_traffic'] = airport_traffic['Flights_from'] + airport_traffic['Flights_to']
# Sort by the airport with the most traffic
airport_traffic_sorted = airport_traffic.sort_values(by='Total_traffic', ascending=False)
# View the top 10 busiest airports by flight traffic
airport_traffic_sorted.head(10)


#this graph connects all of the airports together 
G = nx.DiGraph()
# Add edges for each flight connection, weighted by the number of flights
for _, row in df_2009.iterrows():
    G.add_edge(row['Origin_airport'], row['Destination_airport'], weight=row['Flights'])
# Draw the graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.1)
edge_weights = [G[u][v]['weight'] / 100 for u, v in G.edges()]  # Adjust scaling factor as needed
nx.draw_networkx_edges(G, pos, width=edge_weights)
nx.draw_networkx_nodes(G, pos, node_size=50)
#nx.draw_networkx_edges(G, pos, width=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)
plt.title('US Domestic Air Traffic Network (2009)')
plt.show()


# a graph for the top 25 airports based on total flights
top_airports = airport_traffic_sorted.head(25)['Airport'].tolist()
top_airports_graph = G.subgraph(top_airports)
# Create a dictionary mapping airports to total traffic (used for node size)
node_size_mapping = {row['Airport']: row['Total_traffic'] for _, row in airport_traffic_sorted.iterrows()}
# Set the node sizes based on traffic
# Adjust the scaling factor by dividing by 100 based on how large the values are
node_sizes = [node_size_mapping.get(node, 0) / 100 for node in top_airports_graph.nodes()]
# Draw the subgraph with node sizes based on total traffic
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(top_airports_graph, k=0.5)
# Draw nodes, with size based on total traffic (scaled)
nx.draw_networkx_nodes(top_airports_graph, pos, node_size=node_sizes, node_color='lightblue', alpha=0.8)
# Draw edges (connections between airports)
nx.draw_networkx_edges(top_airports_graph, pos, width=1.0, edge_color='gray')
# Draw labels for airports
nx.draw_networkx_labels(top_airports_graph, pos, font_size=12)
plt.title('Top Airports Network (Node Size Based on Total Flights)')
plt.show()


# Calculate the centrality measures
degree_centrality = nx.degree_centrality(G)
in_degree_centrality = nx.in_degree_centrality(G)
out_degree_centrality = nx.out_degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

# Create dataframes to view the top 10 airports based on each centrality measure
degree_centrality_df = pd.DataFrame(degree_centrality.items(), columns=['Airport', 'Degree_Centrality']).sort_values(by='Degree_Centrality', ascending=False)
in_degree_centrality_df = pd.DataFrame(in_degree_centrality.items(), columns=['Airport', 'In_Degree_Centrality']).sort_values(by='In_Degree_Centrality', ascending=False)
out_degree_centrality_df = pd.DataFrame(out_degree_centrality.items(), columns=['Airport', 'Out_Degree_Centrality']).sort_values(by='Out_Degree_Centrality', ascending=False)
betweenness_centrality_df = pd.DataFrame(betweenness_centrality.items(), columns=['Airport', 'Between_Centrality']).sort_values(by='Between_Centrality', ascending=False)

# Display the top 10 airports for each centrality measure
print("Top 10 Airports by Degree Centrality")
print(degree_centrality_df.head(10))
print("\nTop 10 Airports by In-Degree Centrality")
print(in_degree_centrality_df.head(10))
print("\nTop 10 Airports by Out-Degree Centrality")
print(out_degree_centrality_df.head(10))
print("\nTop 10 Airports by Betweenness Centrality")
print(betweenness_centrality_df.head(10))

# Plot the top 10 airports by degree centrality
top_degree_airports = degree_centrality_df.head(10)['Airport'].tolist()
top_degree_graph = G.subgraph(top_degree_airports)

# Create a dictionary mapping airports to degree centrality (used for node size)
node_size_mapping_degree = {airport: centrality * 1000 for airport, centrality in degree_centrality.items()}

# Draw the subgraph with node sizes based on degree centrality
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(top_degree_graph, k=0.5)
node_sizes_degree = [node_size_mapping_degree.get(node, 0) for node in top_degree_graph.nodes()]

nx.draw_networkx_nodes(top_degree_graph, pos, node_size=node_sizes_degree, node_color='lightgreen', alpha=0.8)
nx.draw_networkx_edges(top_degree_graph, pos, width=1.0, edge_color='gray')
nx.draw_networkx_labels(top_degree_graph, pos, font_size=12)
plt.title('Top 10 Airports by Degree Centrality')
plt.show()
