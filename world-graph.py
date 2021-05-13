import pandas as pd
import numpy as np
from igraph import *


def generateIndex(code):
    try:
        return int(ord(code[0]) * 100 + ord(code[1]))
    except:
        return 0
    

print(generateIndex("TW"))

df = pd.read_csv('./country-borders/GEODATASOURCE-COUNTRY-BORDERS.CSV', index_col=False, header=0)

# print(list(df.columns.values))

# # creates a copy
# label_to_index = df.drop_duplicates(subset=["country_code"])

# # remove index
# label_to_index.pop("country_border_code")
# label_to_index.pop("country_border_name")

# label_to_index_list = label_to_index.values.tolist()

codes_src = list(df["country_code"])
codes_dest = list(df["country_border_code"])

codes = codes_src + codes_dest

code_df = pd.DataFrame(codes, columns=["country_code"])

code_df = code_df.drop_duplicates()

label_to_index_list = list(code_df["country_code"])

index_list = {}

for count, value in enumerate(label_to_index_list):
    index_list[value] = generateIndex(value)

gr = Graph(directed=False)

gr.add_vertices(len(label_to_index_list))

for i, country in enumerate(label_to_index_list):
    gr.vs[i]["id"] = index_list[country]
    gr.vs[i]["name"] = country

edge_list = []

df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

codes_src = list(df["country_code"])
codes_dest = list(df["country_border_code"])

for i, code in enumerate(codes_src):
    edge_list.append((code, codes_dest[i]))
        

gr.add_edges(edge_list)

visual_style = {}

out_name = "graph.png"

# Set bbox and margin
visual_style["bbox"] = (500,500)
visual_style["margin"] = 27

# Set vertex colours
visual_style["vertex_color"] = 'white'

# Set vertex size
visual_style["vertex_size"] = 10

# Set vertex lable size
visual_style["vertex_label_size"] = 5

# Don't curve the edges
visual_style["edge_curved"] = False

# Set the layout
my_layout = gr.layout(layout="auto")
visual_style["layout"] = my_layout

# Plot the graph
plot(gr, out_name, **visual_style)


