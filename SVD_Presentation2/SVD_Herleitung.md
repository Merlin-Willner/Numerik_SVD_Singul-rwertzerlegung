## Mathematische Herleitung der SVD

Gegeben sei eine Matrix

[
A\in\mathbb{R}^{m\times n}
]

Gesucht ist eine Zerlegung der Form

[
\boxed{A=U\Sigma V^T}
]

Dabei sollen (U) und (V) orthogonale Matrizen sein und (\Sigma) eine Diagonalmatrix mit nichtnegativen Einträgen.

---

## 1. Ausgangspunkt: Die Matrix (A^TA)

Wir betrachten zunächst

[
A^TA\in\mathbb{R}^{n\times n}
]

Diese Matrix hat zwei wichtige Eigenschaften.

### Symmetrie

[
(A^TA)^T=A^T(A^T)^T=A^TA
]

Also ist (A^TA) symmetrisch.

### Positive Semidefinitheit

Für jeden Vektor (x\in\mathbb{R}^n) gilt:

[
x^TA^TAx=(Ax)^T(Ax)=|Ax|^2\geq 0
]

Daraus folgt, dass alle Eigenwerte von (A^TA) nichtnegativ sind:

[
\lambda_i\geq 0
]

---

## 2. Spektralsatz auf (A^TA)

Da (A^TA) symmetrisch ist, besitzt sie eine orthonormale Eigenbasis.

Es existieren also Eigenvektoren

[
v_1,\dots,v_n
]

mit

[
A^TAv_i=\lambda_i v_i
]

und

[
v_i^Tv_j=
\begin{cases}
1,&i=j\
0,&i\neq j
\end{cases}
]

Diese Eigenvektoren werden als Spalten in (V) geschrieben:

[
V=
\begin{pmatrix}
| & & |\
v_1 & \cdots & v_n\
| & & |
\end{pmatrix}
]

Da die Spalten orthonormal sind, gilt:

[
V^TV=I
]

und damit

[
V^{-1}=V^T
]

Außerdem kann man (A^TA) diagonalisieren:

[
A^TA=V\Lambda V^T
]

mit

[
\Lambda=
\operatorname{diag}(\lambda_1,\dots,\lambda_n)
]

---

## 3. Definition der Singulärwerte

Da alle Eigenwerte (\lambda_i\geq 0) sind, dürfen wir ihre Quadratwurzeln bilden.

Wir definieren:

[
\boxed{\sigma_i=\sqrt{\lambda_i}}
]

Diese Werte heißen Singulärwerte von (A).

Üblicherweise werden sie absteigend sortiert:

[
\sigma_1\geq \sigma_2\geq\dots\geq 0
]

Die Singulärwerte werden in die Matrix (\Sigma) eingetragen.

Für eine Matrix (A\in\mathbb{R}^{m\times n}) hat (\Sigma) die Form

[
\Sigma\in\mathbb{R}^{m\times n}
]

zum Beispiel:

[
\Sigma=
\begin{pmatrix}
\sigma_1 & 0 & \cdots\
0 & \sigma_2 & \cdots\
\vdots & \vdots & \ddots
\end{pmatrix}
]

---

## 4. Herleitung der linken Singulärvektoren

Aus der Eigenwertgleichung

[
A^TAv_i=\lambda_i v_i
]

und

[
\lambda_i=\sigma_i^2
]

folgt:

[
A^TAv_i=\sigma_i^2v_i
]

Für (\sigma_i>0) definieren wir

[
\boxed{u_i=\frac{Av_i}{\sigma_i}}
]

Damit gilt sofort:

[
Av_i=\sigma_i u_i
]

Das ist eine der zentralen Beziehungen der SVD.

---

## 5. Warum ist (u_i) normiert?

Wir prüfen die Länge von (u_i):

[
|u_i|^2
=======

u_i^Tu_i
]

Einsetzen von

[
u_i=\frac{Av_i}{\sigma_i}
]

ergibt:

[
|u_i|^2
=======

\left(\frac{Av_i}{\sigma_i}\right)^T
\left(\frac{Av_i}{\sigma_i}\right)
]

# [

\frac{1}{\sigma_i^2}
v_i^TA^TAv_i
]

Da

[
A^TAv_i=\sigma_i^2v_i
]

folgt:

[
|u_i|^2
=======

\frac{1}{\sigma_i^2}
v_i^T(\sigma_i^2v_i)
]

# [

v_i^Tv_i
]

Da (v_i) normiert ist:

[
v_i^Tv_i=1
]

also:

[
\boxed{|u_i|=1}
]

---

## 6. Warum sind die (u_i) orthogonal?

Für (i\neq j) gilt:

[
u_i^Tu_j
========

\left(\frac{Av_i}{\sigma_i}\right)^T
\left(\frac{Av_j}{\sigma_j}\right)
]

# [

\frac{1}{\sigma_i\sigma_j}
v_i^TA^TAv_j
]

Mit

[
A^TAv_j=\sigma_j^2v_j
]

folgt:

[
u_i^Tu_j
========

\frac{\sigma_j^2}{\sigma_i\sigma_j}
v_i^Tv_j
]

Da die (v_i) orthogonal sind:

[
v_i^Tv_j=0
]

ergibt sich:

[
\boxed{u_i^Tu_j=0}
]

Die Vektoren (u_i) sind also orthonormal.

Sie bilden die Spalten von (U):

[
U=
\begin{pmatrix}
| & & |\
u_1 & \cdots & u_m\
| & & |
\end{pmatrix}
]

Damit gilt:

[
U^TU=I
]

---

## 7. Zusammensetzen der Gleichungen

Für jeden Singulärvektor gilt:

[
Av_i=\sigma_i u_i
]

Schreibt man alle Gleichungen nebeneinander, erhält man:

[
A
\begin{pmatrix}
| & & |\
v_1 & \cdots & v_n\
| & & |
\end{pmatrix}
=============

\begin{pmatrix}
| & & |\
u_1 & \cdots & u_m\
| & & |
\end{pmatrix}
\Sigma
]

also:

[
AV=U\Sigma
]

Nun multiplizieren wir von rechts mit (V^T):

[
AVV^T=U\Sigma V^T
]

Da (V) orthogonal ist:

[
VV^T=I
]

folgt:

[
\boxed{A=U\Sigma V^T}
]

Damit ist die SVD hergeleitet.

---

## 8. Was passiert bei (\sigma_i=0)?

Falls

[
\sigma_i=0
]

ist, gilt:

[
\lambda_i=0
]

und damit:

[
A^TAv_i=0
]

Außerdem:

[
|Av_i|^2=v_i^TA^TAv_i=0
]

also:

[
Av_i=0
]

Der Vektor (v_i) liegt dann im Kern von (A).

Die Formel

[
u_i=\frac{Av_i}{\sigma_i}
]

kann hier nicht verwendet werden, weil man durch null teilen würde.

Die fehlenden Vektoren in (U) werden stattdessen so ergänzt, dass alle Spalten von (U) weiterhin eine orthonormale Basis bilden.

---

## 9. Kompakte Gesamtidee

Die Herleitung basiert auf:

[
A^TA v_i=\lambda_i v_i
]

Dann setzt man:

[
\sigma_i=\sqrt{\lambda_i}
]

und

[
u_i=\frac{Av_i}{\sigma_i}
]

Dadurch erhält man:

[
Av_i=\sigma_i u_i
]

Für alle Vektoren gleichzeitig:

[
AV=U\Sigma
]

und schließlich:

[
\boxed{A=U\Sigma V^T}
]

---

## Geometrische Bedeutung

Für einen Vektor (x) gilt:

[
Ax=U\Sigma V^Tx
]

Die Transformation läuft in drei Schritten ab:

[
x
\overset{V^T}{\longrightarrow}
V^Tx
\overset{\Sigma}{\longrightarrow}
\Sigma V^Tx
\overset{U}{\longrightarrow}
U\Sigma V^Tx
]

* (V^T): Wechsel in die Basis der rechten Singulärvektoren
* (\Sigma): Streckung oder Stauchung entlang orthogonaler Richtungen
* (U): Wechsel in die Basis der linken Singulärvektoren

Damit beschreibt die SVD jede lineare Abbildung als

[
\boxed{\text{Basiswechsel}\rightarrow\text{Skalierung}\rightarrow\text{Basiswechsel}}
]
