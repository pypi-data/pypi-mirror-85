#TODO versions!

import json
import os
import requests
import time
from collections import OrderedDict

import oda.cache as cache

import oda.sentry as sentry

import pkgutil

import oda.logs as logs
            
import importlib

def log_context(context):
    if logs.logstasher:
        logs.logstasher.set_context(context)

def log(*args, **kwargs):
    logs.log(*args, **kwargs)
    
    if logs.logstasher:
        logs.logstasher.log(dict(event='starting'))

def find_worflow_route_modules():
    workflow_modules = [m for m in pkgutil.iter_modules() if m.name.startswith("oda") and m.name != "oda"]
    log("oda workflow modules: %s", workflow_modules)
    return workflow_modules


def evaluate(router, *args, **kwargs):
    ntries = 100

    key = json.dumps((router, args, OrderedDict(sorted(kwargs.items()))))

    log_context(dict(router=router, args=args, kwargs=kwargs))

    try:
        if router.startswith("oda"):
            module_name = router
        else:
            module_name = 'oda'+router

        odamodule = importlib.import_module(module_name)

        while ntries > 0:
            try:
                output = odamodule.evaluate(*args, **kwargs)
                break
            except Exception as e:
                log(dict(event='problem evaluating',exception=repr(e)))

                if ntries <= 1:
                    if sentry_sdk:
                        sentry_sdk.capture_exception()
                    raise

                time.sleep(5)

                ntries -= 1
    except:
        raise

    log(dict(event='output is None'))

    log(dict(event='done'))

    return output

def evaluate_console():
    import argparse

    argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("router")
        
    args, ukargs = parser.parse_known_args()

    print(args, ukargs)

    pargs=[]
    kwargs={}
    for a in ukargs:
        if a.startswith("--"):
            k, v = a[2:].split("=", 1)
            kwargs[k] = v
        else:
            pargs.append(a)

    print(pargs, kwargs)
    
    return evaluate(args.router, *pargs, **kwargs)

def rdf():
    pass

def apidocs():
    if router == "odahub":
        return requests.get("https://oda-workflows-fermilat.odahub.io/apispec_1.json").json()


def module():
    pass

def module():
    #symmetric interoperability with astroquery
    pass

if __name__ == "__main__":
    evaluate_console()
