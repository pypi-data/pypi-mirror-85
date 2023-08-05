# Benchmark Functions: a Python Collection
A benchmark functions collection wrote in Python 3, suited for assessing the performances of optimisation problems on deterministic functions. Most functions here implemented can be created in an arbitrary number of dimensions. Suggested boundaries, as well the values of known minima/maxima, are also provided. Finally, every function can be visualised with an interactive widget.

## Installation
This module is available on [pip](https://pypi.org/project/benchmark-functions) and can be installed as follows:
```sh
$ pip3 install benchmark_functions
```

## Usage
To use a function from the collection it is sufficient to instantiate the relative class from the library:
```python
import benchmark_functions as bf

func = bf.Schwefel(n_dimensions=4)
```
calling directly the instantiated function on a point will provide the function's value:
```python
point = [25, -34.6, -112.231, 242]
func(point) # results in -129.38197657025287
```
Most functions impelmented can be instantiated with an arbitrary number of dimensions. This can be set with a  *n_dimensions* optional parameter. If the numer of dimensions are not specified a default value (generally $N=2$) will be used.
Some functions require other specific parameters (e.g. Ackley), these can be set in the constructor, otherwise default values will be taken.
Some functions are only defined for 2 dimensions (e.g. Easom) in these cases no *n_dimensions* parameter is accepted.

Normally, these functions are designed for a minimisation problem, so they are designed accordingly.
An optional flag **opposite** can be passed in any function constructor.
If set to *True* the value of the function will be the opposite at each call, as well as the **optimum** value.
This is useful to use a maximisation algorithm on these functions.

A set of convenience functions are also set in the class, namely:

-  **getName** the name of the function
-  **getMinima**/**getMaxima**[^1] a list of tuples (*point*, *value*) with the coordinate and value of the global minima/maxima. If any value is unkown, a *None* value will be present instead.
-  **getMinimum**/**getMaximum**[^1] a single tuple (*point*, *value*) with the coordinate and value of the global minimum/maximum. If any value is unkown, a *None* value will be present instead.
-  **getSuggestedBounds** returns a tuple of two elements (*LB*, *UB*) each one is a list of *n_dimensions* elements, representing the suggested search boundary of the function.
- **show** plot the function in an interactive graphic widget. Read the relative section below for more information on this feature.

As an example, the following code:
```python
print(func.getSuggestedBounds())
```
will produce
```
([-500.0, -500.0, -500.0, -500.0], [500.0, 500.0, 500.0, 500.0])
```
for the Schwefel function.

[^1]: generally a function global minimum/maximum can change with the number of dimensions. For this reason some **minima**/**maxima** values may be missing or inaccurate. If you find a better global optimum please open an issue about that with the coordinates and I'll update the library.
### Visualise a function
Using the *show* function will plot the benchmark function in an interactive widget.
This can be done only if the *n_dimensions* is lower than 3. The resulting plot is either a 3D surface (when *n_dimensions=2*) or a simple 2D graph plot (*n_dimensions=1*). If the function is defined in 2 dimensions, it is also possible to plot it as an heatmap setting the function parameter *asHeatMap=True* as follows:
```python
func.show(asHeatMap=True)
```

Note: whilst importing and using the library require nothing more than the tandard *math* python library, in order to visualise the functions the libraries *mlp_toolkits*, *numpy*, and *matplotlib* are also required.

## List of Available Functions


Name | Image | Description
:---: | :---: | :---
Hypersphere | ![](pics/hypersphere.png) | A simple hypersphere centered in the origin. <br><div align="center">$`f(x)=\sum_{i=1}^N x_i^2`$</div>
Schwefel<sup>[2]</sup> | ![](pics/schwefel.png) |  Non-convex and (highly) multimodal. Location of the minima are geometrical distant.<br><div align="center">$`f(x)=418.9829 N\sum_{i=1}^N x_i\sin(\sqrt{\|x_i\|})`$</div>
Ackley | ![](pics/ackley.png) |  Non-convex and multimodal. Clear global minimum at the center surrounded by many symmetrical local minima. Use three parameters a, b and c. <br><div align="center">$`f(x)=-a\exp\left(-b\sqrt{\frac{1}{N}\sum_{i=1}^N x_i^2}\right)-\exp\left(\frac{1}{N}\sum_{i=1}^N \cos(x_i c)\right)+a+e`$</div>
Michalewicz<sup>[1]</sup> | ![](pics/michalewicz.png) |  Non-convex and (highly) multimodal. Contains n! local minimum. Use a parameter $`m`$ that defines the stepness of the curves. Global minimum around f([2.2,1.57])=-1.8013 for n=2, f(x)=-4.687 for n=5 and f(x)=-9.66 for n=10 (no optimal solution given).<br><div align="center">$`f(x)=-\sum_{i=1}^N \sin(x_i)\sin^{2m}\left(\frac{x_i^2i}{\pi}\right)`$</div>
Rastring<sup>[3]</sup> | ![](pics/rastring.png) |  Non-convex and (highly) multimodal. Location of the minima are regularly distributed.  <br><div align="center">$`f(x)=10N+\sum_{i=1}^N (x_i^2 - 10\cos(2\pi x_i))`$</div>
Rosenbrock<sup>[3]</sup> | ![](pics/rosenbrock.png) |   Non-convex and multimodal. <br><div align="center">$`f(x)=\sum_{i=1}^{N-1} (100(x_{i+1}-x_i^2)^2+(x_i-1)^2`$</div>
De Jong 3 |  ![](pics/dejong3.png) |   Multimodal, "stair"-like function, with multiple plateau at different levels. <br><div align="center">$`f(x)=\sum_{i=1}^{N} \lfloor x_{i}\rfloor `$</div>
De Jong 5<sup>[5]</sup> |  ![](pics/dejong5.png) |   Continuous, multimodal, multiple symmetric local optima with narrow basins on a plateau. It's defined only for 2 dimensions. <br><div align="center">$`f(x)=(0.002+\sum_{i=1}^{25} (i+(x_1-A_{1i})^6+(x_2-A_{2i})^6)^{-1}`$</div>
Griewank<sup>[5]</sup> | ![](pics/griewangk600.png) |   Non-convex and (highly) multimodal, it shows a different behaviour depending on the scale (zoom) that is used. [zoom=0] general overview $`[-600 \leq x_i \leq 600]`$ suggests convex function <br><div align="center">$`f(x)=\sum_{i=1}^{N} \frac{x_i^2}{4000}- \prod_{i=1}^N \cos\frac{x_i}{\sqrt{i}}+1 `$</div>
---- | ![](pics/griewangk10.png) |   [zoom=1] medium-scale view $`[-10 \leq x_i \leq 10]`$ suggests existence of local optima
---- | ![](pics/griewangk5.png) |      [zoom=2] zoom on the details $`[-5 \leq x_i \leq 5]`$ indicates complex structure of numerous local optima
Easom | ![](pics/easom.png) |      Unimodal, mostly a plateau with global minimum in a small central area. It's defined only for 2 dimensions. <br><div align="center">$`f(x)=-\cos(x_1)\cos(x_2)exp(-(x_1-\pi)^2-(x_2-\pi)^2) `$</div>
Goldstein and Price<sup>[6]</sup> | ![](pics/goldstein_price.png) | Multimodal with an asymmetrical hight slope and global minimum on a plateau. It's defined only for 2 dimensions.   <br><div align="center">$`f(x)=(1+(x_1+x_2+1)^2(19-14x_1+3x_1^2-14x_2+6x_1x_2+3x_2^2))\cdot(30+(2x_1-3x_2)^2(18-32x_1+12x_1^2+48x_2-36x_1x_2+27x_2^2)) `$</div>
Picheny, Goldstein and Price<sup>[6]</sup> | ![](pics/picheny_goldstein_price.png) | (logaritmic variant of Goldstein and Price) Non-convex, multimodal with multiple asymmetrical slopes and global minimum near local optima. It's defined only for 2 dimensions.  <br><div align="center">$`f(x)=2.427^{-1}(\log[(1+(x_1+x_2+1)^2(19-14x_1+3x_1^2-14x_2+6x_1x_2+3x_2^2))\cdot(30+(2x_1-3x_2)^2(18-32x_1+12x_1^2+48x_2-36x_1x_2+27x_2^2))]-8.693) `$</div>
Styblinski and Tang | ![](pics/styblinski_tang.png) | Multimodal, with optima displaced in a symmetric way. <br><div align="center">$`f(x)=0.5\sum_{i=1}^{N}(x_i^4-16x_i^2+x_i)`$</div>
Mc Cormick<sup>[7]</sup> | ![](pics/mccormick.png) | Unimodal, uneven slopes on the sides. It's defined only for 2 dimensions. <br><div align="center">$`f(x)=\sin(x_1+x_2)+(x_1-x_2)^2-1.5x_1+2.5x_2+1`$</div>
Rana<sup>[1]</sup> | ![](pics/rana.png) | Highly multimodal symmetric function. <br><div align="center">$`f(x)=\sum_{i=1}^{N-1}x_i\cos\sqrt{\|x_{i+1}+x_i+1\|}\sin\sqrt{\|x_{i+1}-x_i+1\|}+(1+x_{i+1})\sin\sqrt{\|x_{i+1}+x_i+1\|}\cos\sqrt{\|x_{i+1}-x_i+1\|}`$</div>
Egg Holder<sup>[1]</sup> | ![](pics/eggholder.png) | Non-convex, contains multiple asymmetrical local optima. <br><div align="center">$`f(x)=-\sum_{i=1}^{N-1}(x_{i+1}+47)\sin\sqrt{\|x_{i+1}+47+0.5x_i\|}+x_i\sin\sqrt{\|x_i-(x_{i+1}+47)\|}`$</div>
Keane<sup>[1]</sup> | ![](pics/keane.png) | Mutlimodal funciton with local optima regions of different depths.<br><div align="center">$`f(x)=-(\|\sum_{i=1}^{N}\cos^4x_i-\prod_{i=1}^{N}\cos^2x_i\|)(\sum_{i=1}^{N}x_i^2i)^{-\frac{1}{2}}`$</div>

## References

- [1]: Vanaret C., Gotteland J-B., Durand N., Alliot J-M. (2014) [Certified Global Minima for a Benchmark of Difficult Optimization Problems](https://hal-enac.archives-ouvertes.fr/hal-00996713/document). Technical report. Ecole Nationale de l'Aviation Civile. Toulouse, France
- [2]: Schwefel, H.-P.: Numerical optimization of computer models. Chichester: Wiley & Sons, 1981
- [3]: Pohlheim, H. [GEATbx Examples: Examples of Objective Functions](http://www.geatbx.com/download/GEATbx_ObjFunExpl_v37.pdf) 
- [4]: Dixon, L. C. W., & Szego, G. P. (1978). The global optimization problem: an introduction. Towards global optimization, 2, 1-15
- [5]: Molga, M., & Smutnicki, C. [Test functions for optimization needs](http://www.zsd.ict.pwr.wroc.pl/files/docs/functions.pdf) 
- [6]: Picheny, V., Wagner, T., & Ginsbourger, D. (2012). A benchmark of kriging-based infill criteria for noisy optimization.
- [7]: Adorio, E. P., & Diliman, U. P. [MVF - Multivariate Test Functions Library in C for Unconstrained Global Optimization](http://http://www.geocities.ws/eadorio/mvf.pdf)


## Author and License

This library is developed and mantained by Luca Baronti (**gmail** address: *lbaronti*) and released under [GPL v3 license](LICENSE).