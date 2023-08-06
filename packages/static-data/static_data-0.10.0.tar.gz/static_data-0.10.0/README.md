# Static-data
A Python module for those tired of handling ddragon files to get champion/items names/images for League of Legends.

To install, run : 
```
pip3 install static-data
```

OR

Download and run 
```
python setup.py install
```

Use : 

```python
import static_data

dd = static_data.ddragon()

print(dd.getChampion("Annie").image)
print(dd.getChampion(1).image)
print(dd.getChampion(1).name)

print(dd.getChampion("Annie").spell("Q").image)
print(dd.getChampion("Annie").spell(1).image)

print(dd.getSummoner("Flash").image)
#Change the patch to number 4, others settings (season and version) will be set at their last one)
dd.setVersion(patch=4)
print(dd.getSummoner("Flash").image)

#ddragon can be initlized like this : 
dd = ddragon.ddragon(baseUrl="http://ddragon.canisback.com/")
#It will use this url instead of ddragon.leagueoflegends.com ones
```

For now, it only corresponds to my use cases, where I need to get name or image from champion or item having its name or id.

Feel free to ask for more.

Versions : 
 * 0.10.0 : 
     * Adding id for Champion property
 * 0.9.1 : 
     * Fixed the error with icon "placeholder"
     * moved to asyncio to load data faster
 * 0.8.1 : 
     * Fixed the 0.8.0 error.
 * 0.8.0 : 
     * Added rune roots (Domination, Precision...) as simple runes.
     
 * 0.7.0 : 
     * Added an internal cache to use data already called instead of calling it again.
     * Pruned the data to keep only what is useed to save some space in cache.
     * Made ddragon a Singleton.
     
 * 0.6.0 : 
     * Allows to use a local directory (where are stored unziped dragontail files) instead of calling ddragon cdn.
     * Allows to use a local file for versions instead of calling ddragon.leagueoflegends.com/api/versions.json
     
 * 0.5.0 : 
     * Allows to change the base url in the constructor

 * 0.4.0 : 
     * Added runes reforged and fixed icons

 * 0.3.0 : 
     * Added champion spells and icons

 * 0.2.0 : 
 	 * Added summoners spells and maps
 	 * Fix the image url
 	 * Modified the version manager, instead of getLastPatch(), use getPatch(), without argument, to return the last patch Work for version and season as well.