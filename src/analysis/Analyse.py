from src.runner.Loader import TraceLoader
from src.runner.Comparator import Comparator

# load real trace
path_real_trace = "/Users/Nann/workspace/icws2021/src/simulator/traces_real/sample_20o-10c-3333-999.txt"
Loader = TraceLoader(trace_path=)
# load

comparator = Comparator(compare_method="utility", k=2)
comparator.compare( , )

# Analysis here
plt.plot(np.array(time_list_archive), np.array(dists_list_archive))
plt.title("position")
plt.savefig(statistics_dir + "distance_plots{}_{}.pdf".format(seed, human_seed))
plt.close("all")

plt.plot(np.array(time_list_archive), np.array(dists_knowledge_list_archive))
plt.title("global knowledge")
plt.savefig(statistics_dir + "distance_knowledge_plots{}_{}.pdf".format(seed, human_seed))
plt.close("all")

plt.plot(np.array(time_list_archive), np.array(dists_interaction_list_archive))
plt.title("interaction")
plt.savefig(statistics_dir + "distance_interaction_plots{}_{}.pdf".format(seed, human_seed))
plt.close("all")
