import os
import time
import pickle
from functools import wraps

def hashArgsAndKwargs(args, kwargs):
    return hash((args, tuple(kwargs.items())))

class Cache:

    persistent = False
    cache = {}
    filepath = None

    def __init__(self, filename=None, cacheDir=None):
        if cacheDir is not None and filename is not None:
            self.persistent = True
            os.makedirs(cacheDir, exist_ok=True)
            self.filepath = os.path.join(cacheDir, filename)
            self.loadCacheFromFile()

    def loadCacheFromFile(self):
        if os.path.isfile(self.filepath):
            with open(self.filepath, "rb") as f:
                self.cache = pickle.load(f)


    def __contains__(self, key):
        return key in self.cache
    
    def __getitem__(self, key):
        return self.cache[key]["value"]
    
    def __setitem__(self, key, value):
        if key in self:
            self.cache[key]["lastSet"] = time.time()
            self.cache[key]["value"] = value
        else:
            self.cache[key] = {"lastSet": time.time(), "lastGet": time.time(), "value": value}

        if self.persistent:
            with open(self.filepath, "wb") as f:
                pickle.dump(self.cache, f)


    def _invalidationHelper(self, timestamp, whichTimes, howMany=None):
        lastUsed = lambda entry: max(entry[t] for t in whichTimes)
        lru = sorted(self.cache.items(), key=lambda x: lastUsed(x[1]))

        if howMany == None:
            howMany = len(self.cache)
        howMany = min(len(self.cache), howMany)

        i = 0
        while i < howMany and lastUsed(lru[i][1]) < timestamp:
            del self.cache[lru[i][0]]
            i += 1
        
        if self.persistent:
            with open(self.filepath, "wb") as f:
                pickle.dump(self.cache, f)

    def invalidateLastSetBefore(self, firstValidTime):
        """This method invalidates all entries of the cache which were last set sometime before firstValidTime."""
        self._invalidationHelper(firstValidTime, ["lastSet"])
    
    def invalidateLastGotBefore(self, firstValidTime):
        """This method invalidates all entries of the cache which were last got/gotten/accessed (not set) sometime before firstValidTime."""
        self._invalidationHelper(firstValidTime, ["lastGet"])

    def invalidateLastUsedBefore(self, firstValidTime):
        """This method invalidates all entries of the cache which were last accessed (whether mutated or simply queried) before firstValidTime."""
        self._invalidationHelper(firstValidTime, ["lastGet", "lastSet"])


    def invalidateLRU(self, n):
        """This method invalidates the n least recently used (get or set) entries in the cache."""
        self._invalidationHelper(time.time(), ["lastGet", "lastSet"], n)


    def invalidateCall(self, *args, **kwargs):
        key = hashArgsAndKwargs(args, kwargs)
        if key in self.cache:
            del self.cache[key]

            if self.persistent:
                with open(self.filepath, "wb") as f:
                    pickle.dump(self.cache, f)


    def __len__(self):
        return len(self.cache)

    def __repr__(self):
        s = f"filepath: {self.filepath}\n"
        s += f"cache: [\n"
        for entry in self.cache.values():
            lastSet = time.asctime(time.localtime(entry["lastSet"]))
            lastGet = time.asctime(time.localtime(entry["lastGet"]))

            val = entry['value']
            s += f"    (lastSet='{lastSet}', lastGet='{lastGet}', val='{val}')\n"
        s += "]\n"
        return s


def cacheMe(filename=None, cacheDir="__cmoCache__", maxEntries=1_000_000, invalidationStride=1):
    
    def decorator(f):
        pastCalls = Cache(filename, cacheDir)

        @wraps(f)
        def fCached(*args, **kwargs):
            key = hashArgsAndKwargs(args, kwargs)

            if key in pastCalls:
                return pastCalls[key]

            result = f(*args, **kwargs)
            pastCalls[key] = result

            if len(pastCalls) > maxEntries:
                pastCalls.invalidateLRU(invalidationStride)

            return result

        fCached.cmoCache = pastCalls

        return fCached

    return decorator
