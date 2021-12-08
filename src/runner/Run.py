import Main_new


for th in [10, 20, 30, 40, 50, 60, 70, 80]:
    for seed in [200,300,400,500]:
        print("th{}_seed{}".format(th, seed))
        Main_new.main("position", th, seed, 1, estimation_uncertainty=5.0)
