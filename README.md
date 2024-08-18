# beef-to-espanso

Converts a Beeftext backup file (`Beeftext.btbackup`) into Espanso YAML format. 

## Features
- Converts Beeftext combos to Espanso match patterns.
- Cleans up some unusual characters that might be present in the Beeftext backup file.

## Usage

Copy your beeftext backup file to the same directory as the script. 

If the filename is different from `Beeftext.btbackup`, you can specify it with -f.

 ```bash
 python3 beef-to-espanso.py [-f FILENAME]
 ```

 The script will generate YAML files in the `output_groups` directory. You can copy these into your Espanso config folder, and it will automatically load it in.

## License

The code is under the MIT license. You can find it in the `LICENSE` file. 

