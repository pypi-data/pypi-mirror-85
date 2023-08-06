def check_caiman():
    try:
        import caiman

        version = caiman.__version__
        print(f"CaImAn version {version} installed")

    except ImportError:
        print("CaImAn not installed")
    except Exception as ex:
        print("There was an issue with CaImAn")
        raise ex

    try:
        import jobcreator

        version = jobcreator.__version__
        print(f"jobcreator version {version} installed")

    except ImportError:
        print("jobcreator not installed")
    except Exception as ex:
        print("There was an issue with jobcreator")
        raise ex
