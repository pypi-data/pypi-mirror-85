from . import Graph, StateDescriptor, NDPath, Path
from runstats import Statistics
from pprint import pprint

listerator = StateDescriptor(
    constructor=lambda: [],
    updater=lambda x, s: s.append("hello"),
    merger=lambda s1, s2: s1 + s2,
    serializer=lambda s: repr(s),
    deserializer=lambda s: eval(s)
)
statistics = StateDescriptor(
    constructor=lambda: Statistics(),
    updater=lambda x, s: s.push(x[6]),
    merger=lambda s1, s2: s1 + s2,
    serializer=lambda s: s.get_state(),
    deserializer=lambda s: Statistics.fromstate(s),
    extractor=lambda s: s.mean()
)

g1 = Graph(
    state_descriptors={
        'statistics': statistics
    },
    path_extractor=lambda x: {
        'Time': list(x[:3]),
        'Space': list(x[3:6])
    }
)

g2 = Graph(
    state_descriptors={
        'statistics': statistics
    },
    path_extractor=lambda x: {
        'Time': list(x[:3]),
        'Space': list(x[3:6])
    }
)

g1.push([2019, 6, 15, 'a', 'b', 'c', 100])
g2.push([2019, 6, 18, 'x', 'y', 'z', 300])
g2.push([2019, 6, 15, 'x', 'y', 'z', 500])


g1.merge(g2)

edges = g1.edges()
for edge in edges:
    print(edge)

print(g1.get({
    'Time': [2019, 6, 15],
    'Space': []
}))

f = open('graph.csv', 'w')
f.write('Source,Target\n')
for edge in edges:
    f.write(f'{edge[0]},{edge[1]}\n')

s = g1.serialize()

g3 = Graph(
    state_descriptors={
        'statistics': statistics
    },
    path_extractor=lambda x: {
        'Time': list(x[:3]),
        'Space': list(x[3:6])
    }
)

g3.from_serialization(s)
print(g3.get({
    'Time': [2019, 6, 15],
    'Space': []
}))
