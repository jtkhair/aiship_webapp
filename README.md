# Web Application with Data Centric Approach to Ship Powering Prediction using Deep Learning

## Prerequisite
- Interpreter ver.: python 3.6.15
- Container ver.: Docker 20.10.10
- Application ver.: v1.0
- Dependencies: As per listed in requirements.txt

## Introduction
This web application is developed based on the joint work between the [Marine Technology Centre](http://www.mtc-utm.my/)
, Universiti Teknologi Malaysia (UTM) and the [Hiekata Laboratory](https://is.edu.k.u-tokyo.ac.jp/top), University of 
Tokyo (UTokyo) under the UTM research project "Predictive Model for Ship Design and Configuration Using Machine Learning
: Model Development and Validation", project number: Q.J130000.3851.19J88. 

The details of the ship powering prediction modelling is first described in the [research paper](https://bit.ly/3mL96kz) presented in the International Conference on Design and Concurrent Engineering 2021 & Manufacturing System Conference 2021

> _Adi Maimun, Hiekata Kazuo, Jauhari Khairuddin, Siow Chee Loon and Arifah Ali, : "Estimation of Ship Powering in
> Preliminary Ship Design Using Graph Theory and Machine Learning Method". In the International Conference on Design
> and Concurrent Engineering 2021 & Manufacturing System Conference 2021, Sep 2021, Japan_

## Getting started
1. Clone the repo by running this command in the terminal:

```
git clone https://github.com/jtkhair/aiship_webapp
```

2. Make sure to run the command git pull (if you already cloned this repo). In the cloned repo directory, run this 
command in the terminal:
```
git pull https://github.com/jtkhair/aiship_webapp
```

3. Build docker image by running below commands in the terminal (make sure docker is running):
```
cd aiship_webapp
docker build -t aishipwebapp:1.0 .
```

4. Run the docker container by running below command in the terminal:
```
docker run -d --name aishipwebapp -p 80:80 aishipwebapp:1.0
```

5. Go to the link http://0.0.0.0:80 or http://localhost:80 to use the web app

6. Input dataset *.csv file and click submit to perform the prediction. Note that the *.csv file must follow the set 
schema: (['ID', 'LWL', 'B', 'T', 'L/B', 'B/T', 'Disp', 'CB', 'Vs'. 'Fn', 'P']) and example

## Input data format, range and description

Parameter | LWL | B | T | L/B | B/T | Disp | CB |Vs | Fn | P | 
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |
Range | 80 - 240 | 15 - 32 | 3 - 8 | 3.5 - 9.0 | 3.0 - 5.5 | 2500 - 32000 | 0.5 - 0.7 | 14.5 - 30.5 | 0.20 - 0.40 | 3000 - 70000 | 

## Input data example

ID | LWL | B | T | L/B | B/T | Disp | CB | Vs | Fn | P 
--- | --- | --- |--- |--- |--- |--- |--- |--- |--- |--- |
INPUT_80_1 | 80 | 12.4 | 4.4 | 6.45 | 2.82 | 1712 | 0.39 | 10 | 0.18 | Nan 

### Acronym
- Waterline length in m, LWL
- Breadth at waterline in m, B
- Draught in m, T
- Length-to-breadth ratio, L/B
- Breadth-to-draught ratio, B/T
- Displacement in t, Disp
- Block coefficient, CB
- Service speed in kn, Vs
- Froude number, Fn
- Brake kilowatt power in kW, P

## Acknowledgement
> This work is funded by the Universiti Teknologi Malaysia (UTM) under the Research University Grant (RUG).
Project number: Q.J130000.3851.19J88 and titled: “Predictive Model for Ship Design and Configuration Using Machine
Learning - Model Development and Validation”
