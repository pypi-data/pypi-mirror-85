# TP Importer

This package is used for importing our main Titelplanung Excel file;
<br>
as this data is used in different systems this package provides adapters to use the imported data within different products
<br>
## Usage
Usage Example:
```
def import_tp_data_for_mam():
    tp_path = "G:\Listen\TPDD aktuell absolutiert.xlsm"
    tp_data = TP_Importer().get_tp_data_from_file(tp_path)
    tp_data_mam = Adapter_For_MAM().transform(tp_data)
    for title in tp_data_mam:
        print(title)


if __name__ == '__main__':
    tp_data_mam = import_tp_data_for_mam()
```