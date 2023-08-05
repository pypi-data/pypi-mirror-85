# Conductor for Maya

Maya plugin submitter for the Conductor Cloud rendering service.

## Install

**To install the latest version.**
```bash
pip install --upgrade ciomaya --target=$HOME/Conductor
```

**To install a specific version, for example 0.1.0.**
```bash
pip install --upgrade --force-reinstall ciomaya==0.1.0 --target=$HOME/Conductor
```

**Then setup the Maya module.** 

```bash
python ~/Conductor/ciomaya/post_install.py
```

## Usage

Open the Plugin Manager and load **Conductor.py**.

Go to **Conductor->About** to check the version and other info.

To set up a render, choose **Conductor->Submitter->Create** from the **Conductor** menu. 

For detailed help, checkout the [tutorial](https://docs.conductortech.com/tutorials/maya_beta) and [reference](https://docs.conductortech.com/reference/maya_beta) documentation.

## Contributing

For help setting up your dev environment please visit [https://docs.conductortech.com/dev/contributing](https://docs.conductortech.com/dev/contributing)

Pull requests are welcome. For major changes, please [open an issue](https://github.com/AtomicConductor/conductor-maya/issues) to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit)