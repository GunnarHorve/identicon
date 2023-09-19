
## pallette_names.jon
When visiting [seaborn's color palettes](https://www.practicalpythonfordatascience.com/ap_seaborn_palette#all-palettes) and considering their API, I found it more convenient to rip all color palette names from their website, rather than call the several hidden variables/naming schemas they used to define their palette strings
```javascript
# throw all palette strings into a clipboard, then dump to palette_names.json
copy(Array.from(document.getElementsByClassName("s1")).map(span => span.textContent))
```
