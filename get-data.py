from arctic import Arctic
import pandas as pd
import tqdm

db = Arctic("localhost")

libs = db.list_libraries() 

print (libs) 

libs_to_use = ["Bloomberg.EOD","Bloomberg.EOD_Unadjusted","Bloomberg.Adjustments",
"Bloomberg.Corporate_Actions","Bloomberg.Metadata",'Bloomberg.Indexes_Members','Bloomberg.References']



def extract_EOD(libName,folder):

    lib = db[libName]

    tickers = lib.list_symbols()

    for ticker in tqdm.tqdm(tickers):
        # df = lib.read(symbol= ticker)
        dataname = " ".join(ticker.split(" ")[:1]) 
        # print ( dataname)
        df = lib.read(symbol=ticker)
        df.to_csv("{}/{}.csv".format(folder,dataname))


def rename(name):
        return name.split(" ")[0]

def extract_composition(libName):

    
    
    lib = db[libName]
    # print (lib.list_symbols())
    df = lib.read(symbol="MOSENEW Index")

    df.index_member = df.index_member.apply(rename)
    df.drop(columns = ["symbol"], inplace = True)
    df.to_csv("composition.csv")

def extract_corporate_Actions(libName):
    lib = db[libName]
    tickers = lib.list_symbols()
    ldf = []

    for ticker in tickers:
        df = lib.read(symbol = ticker).data
        
        df["symbol"] = rename(ticker)
        df.reset_index(inplace=True)
        df.drop(inplace=True,columns=['index'])
        # print (df.tail())
        ldf.append(df)
    data = pd.concat(ldf)
    data.to_csv("corporate_actions.csv")

if __name__ == "__main__":

    EOD_library = libs_to_use[0]
    folder = 'data'
    # extract_EOD(libName=EOD_library,folder=folder)

    EOD_unadjusted_library = libs_to_use[1]
    folder = 'data_unadjusted'
    # extract_EOD(libName=EOD_unadjusted_library,folder=folder)

    Benchmark_Composition_library = libs_to_use[-2]

    # extract_composition(libName=Benchmark_Composition_library)

    Corporate_Actions_library = libs_to_use[3]
    # print (Corporate_Actions_library)

    extract_corporate_Actions(libName=Corporate_Actions_library)








