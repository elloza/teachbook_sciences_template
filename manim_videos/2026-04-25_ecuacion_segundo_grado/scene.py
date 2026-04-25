from manim import *
import numpy as np


class QuadraticEquation(Scene):
    def construct(self):
        # Título
        title = Text("La Ecuación de Segundo Grado", font_size=40)
        self.play(Write(title))
        self.wait(1)

        # Forma general
        eq_text = MarkupText("ax<sup>2</sup> + bx + c = 0", font_size=60)
        self.play(Write(eq_text))
        self.wait(2)

        self.play(eq_text.animate.shift(UP * 2))

        # La fórmula resolvente
        formula_text = Text("Fórmula general:", font_size=36).next_to(eq_text, DOWN, buff=0.5)
        formula = MarkupText(
            "x = (-b ± √(b<sup>2</sup> - 4ac)) / 2a", font_size=40
        ).next_to(formula_text, DOWN, buff=0.5)

        self.play(FadeIn(formula_text))
        self.play(Write(formula))
        self.wait(2)

        # El discriminante
        disc_text = Text("El discriminante (Δ):", font_size=36).next_to(formula, DOWN, buff=0.5)
        discriminant = MarkupText("Δ = b<sup>2</sup> - 4ac", font_size=50).next_to(disc_text, DOWN, buff=0.5)
        discriminant.set_color(YELLOW)

        self.play(FadeIn(disc_text))
        self.play(Write(discriminant))
        self.wait(2)

        self.play(FadeOut(eq_text), FadeOut(formula_text), FadeOut(formula), FadeOut(disc_text))
        self.play(discriminant.animate.move_to(UP * 1.5))
        self.wait(1)

        # Casos
        case1 = MarkupText("Si <span fgcolor='green'>Δ &gt; 0</span>: Dos soluciones reales", font_size=30).next_to(discriminant, DOWN, buff=0.8)
        case2 = MarkupText("Si <span fgcolor='blue'>Δ = 0</span>: Una solución real doble", font_size=30).next_to(case1, DOWN, buff=0.5)
        case3 = MarkupText("Si <span fgcolor='red'>Δ &lt; 0</span>: Sin soluciones reales", font_size=30).next_to(case2, DOWN, buff=0.5)

        self.play(Write(case1))
        self.wait(1.5)
        self.play(Write(case2))
        self.wait(1.5)
        self.play(Write(case3))
        self.wait(3)

        self.play(FadeOut(Group(title, discriminant, case1, case2, case3)))

        # Parábolas de ejemplo
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 6, 1],
            x_length=7,
            y_length=5,
            axis_config={"color": WHITE},
        ).shift(DOWN * 0.5)

        self.play(Create(axes))

        # Dos soluciones (intersecta x dos veces) y = x^2 - 1
        graph1 = axes.plot(lambda x: x**2 - 1, color=GREEN)
        label1 = Text("Δ > 0", color=GREEN, font_size=30).to_corner(UR)

        self.play(Create(graph1), Write(label1))
        self.wait(2)

        # Una solución (intersecta x una vez) y = x^2
        graph2 = axes.plot(lambda x: x**2, color=BLUE)
        label2 = Text("Δ = 0", color=BLUE, font_size=30).to_corner(UR)

        self.play(ReplacementTransform(graph1, graph2), ReplacementTransform(label1, label2))
        self.wait(2)

        # Sin soluciones (no intersecta x) y = x^2 + 1
        graph3 = axes.plot(lambda x: x**2 + 1, color=RED)
        label3 = Text("Δ < 0", color=RED, font_size=30).to_corner(UR)

        self.play(ReplacementTransform(graph2, graph3), ReplacementTransform(label2, label3))
        self.wait(2)

        self.play(FadeOut(Group(axes, graph3, label3)))
        self.wait(1)
