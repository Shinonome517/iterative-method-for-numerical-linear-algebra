---
marp: true
theme: gaia
---
<!-- paginate: true -->
<!-- footer: RICORA PROGRAMMING TEAM -->

# 第9回数値解析班輪講

連立一次方程式の解法2 ~疎行列と反復法~

---

## 輪講の目的

### 目的二つ

1. 数値計算について学ぶ
2. Pythonの使用経験を積む

### やっていること

1. 定理の証明・アルゴリズムの勉強（数学）
2. 実装（プログラミング）

---

## 数値計算とは

*連続数学への離散的アプローチ*

微分方程式の数値解法

* Eular法
* Runge-Kutta法

![bg right:45%](./pictures/eular-runge.png)


---

## 本日のお品書き

### データ構造

* 疎行列とは
* 疎行列のデータ構造

### 反復法（アルゴリズム）

* 反復法とは
* ヤコビ法
* ~~共役勾配法~~

---

## 本題

![bg right:70%](./pictures/kusatsu.JPG)

---

## 疎行列とは


![bg 80%](pictures/mumplus.png)
![bg 80%](pictures/matrix1.png)

---

## 疎行列のデータ形式

通常の二次元配列だと無駄が多い

↓

データを圧縮した形で保存する

---

## 疎行列のデータ形式

次の行列を疎行列特有の形式で保存する

$$

A = 
\begin{pmatrix}
1 & 0 & 2 & 0 & 0 \\
0 & 3 & 0 & 0 & -4 \\
0 & 0 & 5 & 0 & 0 \\
6 & 0 & 0 & -7 & 0 \\
0 & 0 & 0 & 0 & 8
\end{pmatrix}

$$

---

## 疎行列のデータ構造

### COO方式(sparse matrix in **COO**rdinate format)

データ、行番号、列番号、をそれぞれリストで保管

```Python
data[] = [1, 2, 3, -4, 5, 6, -7, 8]
row[] = [0, 0, 1, 1, 2, 3, 3, 4]
col[] = [0, 2, 1, 4, 2, 0, 3, 4]
```

ex) $a_{25} = -4$ 

---

## 疎行列のデータ構造

### CSR方式(**C**ompressed **S**parse **R**ow Matrix)

データ、列番号、行が切り替わるデータの場所、をそれぞれリストで保管

```Python
data[] = [1, 2, 3, -4, 5, 6, -7, 8]
indices[] = [0, 2, 1, 4, 2, 0, 3, 4]
indptr[] = [0, 2, 4, 5, 7, 8]
```

data[] = [|1, 2, |3, -4, |5, |6, -7, |8]

---

## 疎行列のデータ構造

### CSC方式(**C**ompressed **S**parse **C**olumn Matrix)

データ、行番号、列が切り替わるデータの場所、をそれぞれリストで保管

```Python
data[] = [1, 6, 3, 2, 5, -7, -4, 8]
indices[] = [0, 3, 1, 0, 2, 3, 1, 4]
indptr[] =  [0, 2, 3, 5, 6, 8]
```

data[] = [|1, 6, |3, |2, 5, |-7, |-4, 8]

---

## 疎行列のデータ構造



### 実装

手元で見せます

[ShinonomeのGitHub](https://github.com/Shinonome517/iterative-method-for-numerical-linear-algebra)

---

## 疎行列のデータ構造

### 実行結果

VSCodeの画面、又は、GitHubからCloneして手元で実行

---

## 前半終了

質問等があれば受け付けます。

---

## 反復法とは

問題$A\bf{x} - \bf{b}$

- 直接法：行列Aを直接変形して解を得る

    有限回の操作で必ず実行が終わる

- 反復法：問題の解と同じ値を収束値に持つ漸化式を作成し、反復計算をして解を得る

    原理的には解を得るために無限回の操作が必要
    →「収束判定がある」    

---

## 反復法とは

もっと具体的に反復法を規定する。

>連立一次方程式
>
>$$ A \bf{x} = \bf{b} $$
>
>が与えられた時、この解の近似解$x_{k+1}$を漸化式
>
>$$ \bf{x_{k+1}} = M \bf{x_k} + \bf{c} $$
>
>で計算する方法を反復法という

---

## 反復法とは

>ただし、この$M$と$\bf{c}$は上記の漸化式の収束値が
>連立一次方程式 $A \bf{x} = \bf{b}$の解と同じになるように設定する。
>
>即ち、以下二式の解$\bf{x}$が一致するように$M$と$\bf{c}$を定める
>
>$$ 
>\begin{aligned}
>    M\bf{x} + \bf{c} &= \bf{x} \\
>    A \bf{x} &= \bf{b} \\
>\end{aligned}
>$$

---

## 反復法とは

教科書そのままだと、流れが見づらいので整理する

$$A \bf{x} = \bf{b}$$

に対して、

$$M \bf{x}  + \bf{c} = \bf{x} $$

を満たすように$M$と$\bf{c}$を頑張って構成

---

## 反復法とは

ここで

$$ \bf{x_{k+1}} = M \bf{x_k} + \bf{c} $$

が収束すれば、その収束値$\bf{x^*}$は$M \bf{x}  + \bf{c} = \bf{x}$を満たすため
収束値が$A \bf{x} = \bf{b}$の解になる。

---

## 反復法とは

問題は、この漸化式(1)$\bf{x_{k+1}} = M \bf{x_k} + \bf{c}$から得られる数列が収束するのか否かである

いくつか数学的な準備をする

---

## 反復法とは

### ＜定義＞ スペクトル半径

$\mathbb{K}$を体とし、$A$を $A \in \mathbb{K^{n \times n}}$の正方行列とする
$A$ の固有値を $\lambda_1, \lambda_2, ... \lambda_n$ とするとき
これらの固有値の絶対値の中の最大値を$A$のスペクトル半径といい、$\rho(A)$で表す
すなわち

$$ \rho(A) = \max_{1 \leq i \leq n} |\lambda_i|$$

---

## 反復法とは

### 命題 スペクトル半径と行列の極限（証明略）

$A \in \mathbb{C^{n \times n}}$について、

$$\lim_{k \rightarrow \infty} A^k = O$$

と

$$\rho(A) < 1$$

は同値

---

## 反復法とは 

### ＜定理＞ 漸化式の収束の為の必要十分条件

任意の初期値$x_0$に対して、漸化式(1)

$$\bf{x_{k+1}} = M \bf{x_k} + \bf{c}$$ 

から得られる数列${x_k}$が収束する為の必要十分条件は

$$ \rho(M) < 1 $$

である。

---

## 反復法とは

＜証明＞

$$
\begin{cases}
    \bf{x_k} &= M\bf{x_{k-1}} + \bf{c} \\
    \bf{x} &= M \bf{x}  + \bf{c}
\end{cases}
$$

より、

$$\bf{x_k} - \bf{x} = M (\bf{x_{k-1}} - \bf{x})$$

---

## 反復法とは

これを繰り返し用いて

$$\bf{x_k} - \bf{x} = M^k (\bf{x_0} - \bf{x})$$

---

## 反復法とは

これより

$$
\begin{aligned}
    &\lim_{k \rightarrow \infty} \bf{x_k} = \bf{x}  \\
    \Leftrightarrow &\lim_{k \rightarrow \infty} M^k(\bf{x_0} - \bf{x}) + \bf{x} = \bf{x} \\
    \Leftrightarrow&\lim_{k \rightarrow \infty} M^k = O \\
    \Leftrightarrow&\rho(M) < 1
\end{aligned}
$$

---

## ヤコビ反復法

### ＜アルゴリズム＞ ヤコビ反復法

1. 初期値$x_0 \in \mathbb{R}^n$を与える
2. **収束するまで** 以下の漸化式を計算する
>各$x_k (1 \leq k \leq n)$について
>$$\bf{x_k^{(m+1)}} = \frac{1}{a_{k,k}} \left( \bf{b_k} - \sum_{j \neq i } a_{i,j}x_j^{(m)} \right)

---

## ヤコビ反復法

これを反復法の漸化式の形

$$\bf{x_{k+1}} = J\bf{x_{k}} + \bf{c}$$

で書くと、

$$ J = [k_{i, j}] = 
\begin{cases} 
0& (i = j) \\
-\frac{a_{i, j}}{a_{i, i}}& ( i \neq j)
\end{cases}
$$

---

## ヤコビ反復法

$$
\bf{c} = \left( \frac{b_1}{a_{1, 1}}, \frac{b_2}{a_{2, 2}}, ... \frac{b_n}{a_{n, n}} \right)^\top
$$

---

## ヤコビ反復法

先の収束のための必要十分条件を求めるためには、固有値を求めなければならない

↓

実は非常に困難

---



---

### 実装

手元で見せます

[ShinonomeのGitHub](https://github.com/Shinonome517/iterative-method-for-numerical-linear-algebra)

---

## 参考資料

「Python数値計算プログラミング」幸谷智紀 2021 講談社

「数値解析入門」齊藤宣一 2012 東大出版

[Scipyのsparseモジュールについて](https://hamukazu.com/2014/12/03/internal-data-structure-scipy-sparse/)

---

## ご清聴ありがとうございました

---