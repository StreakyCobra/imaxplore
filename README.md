# Imaxplore

Requirements:

- qt4 & pyqt4
- numpy
- matplotlib

This can be installed easily with conda by using:

```sh
$ conda create -n pyqt pyqt=4 numpy matlpotlib scikit-image 
```

Before running the `.po` files should be compiled to `.mo` by calling: `msgfmt -o imaxplore.mo imaxplore.po` in each language folder.
