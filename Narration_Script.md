# Narration Script — Eigenvalues & Eigenvectors

**Target Pace:** ~140 words/minute (~700 words total for a 5:10 video)  
**Delivery Style:** Conversational, clear, fellow-engineering-student tone. Every symbol is defined before it is used, and each step explains *why*, not just *what*.

---

## Scene 1: Opening Frame & Hook `[0:00 – 0:30]` (~65 words)

- **`[0:00 – 0:06]` (Opening Frame)**  
  Welcome to this M3 Linear Algebra visual guide on eigenvalues and eigenvectors.

- **`[0:06 – 0:16]`**  
  Think of a matrix $A$ as a machine that warps space—stretching, shearing, and rotating every vector on the grid. Watch what happens when we apply the matrix $A = \begin{bmatrix}2 & 1 \\ 1 & 2\end{bmatrix}$ to five ordinary vectors.

- **`[0:16 – 0:30]`**  
  Almost every vector gets knocked off its original path. Look at $(1,0)$ and $(0,1)$—they swing inward. Yet two special vectors, shown in orange and teal, never leave the straight lines they started on. That raises our central question: **which directions survive a transformation?**

---

## Scene 2: Concept Introduction `[0:30 – 1:15]` (~105 words)

- **`[0:30 – 0:38]`**  
  By the end of this video, you will be able to explain what an eigenvector is geometrically and compute both eigenvalues and eigenvectors for any 2-by-2 matrix.

- **`[0:38 – 0:54]`**  
  In linear algebra, that surviving-direction property is captured by one compact equation: $A\mathbf{v} = \lambda\mathbf{v}$.  
  Here, $A$ is our 2-by-2 transformation matrix. $\mathbf{v}$ is a nonzero vector called an **eigenvector**—from the German word *eigen*, meaning "own" or "characteristic." And the Greek letter $\lambda$—lambda—is a scalar number called the **eigenvalue**, which measures how much $\mathbf{v}$ scales. Notice we require $\mathbf{v} \neq \mathbf{0}$, because $A\mathbf{0} = \lambda\mathbf{0}$ is trivially true for any $\lambda$ and tells us nothing about direction.

- **`[0:54 – 1:15]`**  
  Geometrically, multiplying an eigenvector $\mathbf{v}$ by $A$ produces the exact same result as multiplying $\mathbf{v}$ by the scalar $\lambda$: $\mathbf{v}$ stays on its own span line, whereas an ordinary vector $\mathbf{u}$ gets rotated off its line.

---

## Scene 3: Visual Intuition `[1:15 – 2:30]` (~170 words)

- **`[1:15 – 1:25]`**  
  Let's see this unfold continuously on the unit grid. We start with our un-deformed reference grid in the background and five test vectors, each resting on its own dashed span line. On the right, we track $\Delta\theta$—the angle each vector turns away from its starting line.

- **`[1:25 – 1:45]`**  
  As our parameter $t$ sweeps smoothly from zero to one, the grid interpolates from the identity matrix $I$ to $A$. Watch the grey vectors: $(1,0)$ turns to $(2,1)$, $(0,1)$ turns to $(1,2)$, and $(2,-1)$ swings all the way to $(3,0)$. Every single one peels away from its dashed line, with nonzero angle changes.

- **`[1:45 – 2:10]`**  
  Now focus on the two vectors that stay at $\Delta\theta = 0^\circ$. The orange vector $\mathbf{v}_1 = (1,1)$ glides straight along the line $y = x$ out to $(3,3)$—three times its original length. Meanwhile, the teal vector $\mathbf{v}_2 = (1,-1)$ sits completely unchanged at $(1,-1)$, scaled by a factor of one.

- **`[2:10 – 2:30]`**  
  Visualizing the grid makes it clear *what* eigenvectors are. But for an arbitrary 2-by-2 matrix in an exam or engineering model, we can't just eyeball a grid. So how do we find $\lambda$ and $\mathbf{v}$ algebraically? We turn the geometry into the characteristic equation $\det(A - \lambda I) = 0$.

---

## Scene 4: Worked Example `[2:30 – 4:00]` (~215 words)

- **`[2:30 – 2:42]`**  
  Let's solve $A = \begin{bmatrix}2 & 1 \\ 1 & 2\end{bmatrix}$ step by step. Start from $A\mathbf{v} = \lambda\mathbf{v}$. To subtract $\lambda\mathbf{v}$ from $A\mathbf{v}$, we insert the 2-by-2 identity matrix $I$, turning the scalar $\lambda$ into $\lambda I$. Factoring out $\mathbf{v}$ gives $(A - \lambda I)\mathbf{v} = \mathbf{0}$. Why does the determinant matter here? Because if $(A - \lambda I)$ were invertible, the only solution would be $\mathbf{v} = \mathbf{0}$. To allow a nonzero eigenvector $\mathbf{v}$, the matrix $(A - \lambda I)$ must squash space—meaning its determinant must equal zero.

- **`[2:42 – 3:12]`**  
  First, subtract $\lambda I$ from $A$: we subtract $\lambda$ down the main diagonal to get $\begin{bmatrix}2-\lambda & 1 \\ 1 & 2-\lambda\end{bmatrix}$. Taking the 2-by-2 determinant—product of the main diagonal minus the off-diagonal—gives $(2-\lambda)^2 - 1 = 0$. Expanding $(2-\lambda)^2$ yields $4 - 4\lambda + \lambda^2 - 1 = 0$, which simplifies to the characteristic polynomial $\lambda^2 - 4\lambda + 3 = 0$. This factors cleanly into $(\lambda - 3)(\lambda - 1) = 0$, giving two eigenvalues: $\lambda_1 = 3$ and $\lambda_2 = 1$.

- **`[3:12 – 3:36]`**  
  Now we find the eigenvector for $\lambda_1 = 3$. Substitute $\lambda = 3$ into $(A - \lambda I)\mathbf{v}_1 = \mathbf{0}$. Subtracting 3 from the diagonal gives $\begin{bmatrix}-1 & 1 \\ 1 & -1\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix} = \begin{bmatrix}0 \\ 0\end{bmatrix}$. Notice both rows give the exact same equation: $-x + y = 0$, so $y = x$. Any nonzero multiple works, so picking $x = 1$ gives $\mathbf{v}_1 = \begin{bmatrix}1 \\ 1\end{bmatrix}$. Let's check by substitution: $A\begin{bmatrix}1 \\ 1\end{bmatrix} = \begin{bmatrix}2+1 \\ 1+2\end{bmatrix} = \begin{bmatrix}3 \\ 3\end{bmatrix} = 3\begin{bmatrix}1 \\ 1\end{bmatrix}$. Exact match!

- **`[3:36 – 4:00]`**  
  Next, substitute $\lambda_2 = 1$ into $(A - I)\mathbf{v}_2 = \mathbf{0}$. Subtracting 1 from the diagonal gives $\begin{bmatrix}1 & 1 \\ 1 & 1\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix} = \begin{bmatrix}0 \\ 0\end{bmatrix}$. Here both rows say $x + y = 0$, or $y = -x$. Choosing $x = 1$ gives $\mathbf{v}_2 = \begin{bmatrix}1 \\ -1\end{bmatrix}$. Checking by substitution: $A\begin{bmatrix}1 \\ -1\end{bmatrix} = \begin{bmatrix}2-1 \\ 1-2\end{bmatrix} = \begin{bmatrix}1 \\ -1\end{bmatrix} = 1\begin{bmatrix}1 \\ -1\end{bmatrix}$. Verified!

---

## Scene 5: Interpretation `[4:00 – 4:45]` (~105 words)

- **`[4:00 – 4:20]`**  
  Connecting the algebra back to our grid: the eigenvalues $\lambda_1 = 3$ and $\lambda_2 = 1$ are literally the scaling factors along those two invariant axes—$(1,1)$ stretches threefold while $(1,-1)$ stays fixed. And notice the right angle at the origin: because $A$ is symmetric, its eigenvectors are perpendicular.

- **`[4:20 – 4:35]`**  
  What if we had seen other values of $\lambda$? An eigenvalue between zero and one shrinks the vector toward the origin. An eigenvalue of zero collapses that entire eigenline down to the zero vector, making $\det(A) = 0$. And a negative eigenvalue—like $\lambda = -2$—flips the vector 180 degrees to point the opposite way along the exact same line.

- **`[4:35 – 4:45]`**  
  That single idea powers huge parts of engineering: natural vibration modes in structures, Principal Component Analysis in machine learning, and even Google's PageRank algorithm.

---

## Scene 6: Summary & Credits `[4:45 – 5:10]` (~50 words)

- **`[4:45 – 4:58]`**  
  To recap three takeaways: first, eigenvectors keep their direction under $A$, satisfying $A\mathbf{v} = \lambda\mathbf{v}$. Second, find $\lambda$ from $\det(A - \lambda I) = 0$, then solve $(A - \lambda I)\mathbf{v} = \mathbf{0}$ for $\mathbf{v}$. Third, $\lambda$ tells you the scaling factor along each invariant line.

- **`[4:58 – 5:10]`**  
  Thank you for watching. References and course details are shown here on screen.
