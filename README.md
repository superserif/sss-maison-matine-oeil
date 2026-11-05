# Maison Matine — l'œil du footer

Footer de la page produit Maison Matine, avec l'œil de la lampe animé.

- la pupille suit le curseur (au doigt : le point touché) et passe sous les paupières quand elle regarde haut ou bas ;
- il cligne tout seul, parfois deux fois, et quand le regard saute d'un bout à l'autre de l'écran ;
- au clic (ou au tap) il se ferme d'un coup, reste fermé, rouvre à moitié pour vérifier, puis en grand ; trois clics de suite et il boude plus longtemps ;
- curseur tout près : il plisse l'œil ; on tape son e-mail : il lit ce qu'on écrit ; on s'inscrit : clin d'œil ;
- sans rien bouger pendant 9 s il s'assoupit, lutte un peu, puis s'endort ; il se réveille au premier geste ;
- en mobile, la frise est recomposée autour de la lampe pour que l'œil reste lisible.

`index.html` est autonome (seules les polices viennent de Google Fonts). Pour le régénérer après une modification :

```bash
python3 build.py
```

- `src/page.html` : la page et le script de l'œil ;
- `svg/illu-1.svg` : la frise (sans l'œil) ; `illu-2.svg` la pupille ; `illu-4.svg` l'amande et son contour (`illu-3.svg` : l'œil complet, pour référence) ;
- `vendor/lenis.min.js` : défilement amorti, mis en ligne dans la page.

Depuis la console : `__eye.poke()`, `__eye.doze()`, `__eye.wake()`.
