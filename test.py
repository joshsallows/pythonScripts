items_cost = [ 999,888,1100,1200,1300,777]

items_cost_with_gst = list(map(lambda x:x*1.07, items_cost))
print(items_cost)
print(items_cost_with_gst)
print(list(map(lambda x,y:x+y,items_cost,items_cost_with_gst)))



