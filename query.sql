-- IMPORTANT  : la table match_principale -> match

-- Quels sont les investisseurs les plus actifs (nombre de startups rencontrées) ?

select count(DISTINCT(match.startup_id)) as "Total recommendation" , investisseur.nom as Nom
from match
join investisseur
on investisseur.ID_investisseur = match.investisseur_ID
group by Nom
order by "Total recommendation" desc limit 3;


-- Combien de matchs sont à relancer selon leur typologie d'investisseur (VC, BA, Banque…) ?

select typologie.typologie as "Typologie", count(match.id_match) as total
from match
join typologie on typologie.id_typologie = match.typologie_id
join statut_match on statut_match.ID_statut_match = match.statut_match_id
where  statut_match.statut_match = "relancer" and typologie.typologie is not null
group by "Typologie" 
order by total DESC;

"""

gestion des valeurs vides dans la colonne typologie :

select * from typologie
UPDATE typologie
SET typologie = 'Pas de typologie'
WHERE typologie = ''

"""

-- Quelle part des startups est en phase de deal ou de contact établi ?
-- Quelle startup a suscité le plus d’intérêt (nombre de contacts investisseurs) ?







SELECT COUNT(startup.nom) AS "statup star", investisseur.nom AS "Investisseur"


select startup, count(investisseur_statut) as Count
from raw_data
where investisseur_statut = 'Contacté'
group by "startup"
order by Count desc;

'''on se rencompte que les colonne qui portent le meme nom que la table, posent beaucoup de pb .
Il faut changer leur noms (Nettoyage en SQL)
-- ALTER TABLE investisseur RENAME COLUMN investisseur TO nom; --
'''

-- Quel est le pourcentage d'investisseurs n'ayant jamais été relancés (statut = "Vivier") ?
-- Y a-t-il une corrélation entre le type d’investisseur et la probabilité d’aboutir à un deal ?

'''
transformation des données en SQL de la table RAW_DATA :

ALTER TABLE raw_data RENAME COLUMN "Id. unique" TO id_unique;
ALTER TABLE raw_data RENAME COLUMN "Id.Match" TO id_match;
ALTER TABLE raw_data RENAME COLUMN "Start-up" TO startup;
ALTER TABLE raw_data RENAME COLUMN "Id.Startup" TO id_startup;
ALTER TABLE raw_data RENAME COLUMN "Id.Investisseur" TO id_investisseur;
ALTER TABLE raw_data RENAME COLUMN "Investisseur.statut" TO investisseur_statut;
ALTER TABLE raw_data RENAME COLUMN "Statut match" TO statut_match;
ALTER TABLE raw_data RENAME COLUMN "RDV le" TO rdv_le;
ALTER TABLE raw_data RENAME COLUMN "contact investisseur" TO contact_investisseur;
'''




-- nombre de relation par startup
select count(*) as "Total relation", startup from raw_data
group by startup
order by "Total relation" DESC

-- Camembert des typologies d’investisseurs engagés.

select typologie, count(typologie) as "nombre d'occurence" from raw_data 
where statut_match= 'Deal'
group by typologie
order by "nombre d'occurence" DESC;

SELECT Typologie, COUNT(DISTINCT investisseur) AS nb_investisseurs
FROM raw_data
GROUP BY Typologie;


select investisseur, typologie, statut_match from raw_data 
where statut_match= 'Deal';

-- Tableau des investisseurs à relancer.

Select i.nom as "Nom d'investisseur" ,
	   s.statut_match as "statut investisseur",
	   count(*) as "Nombre"
from investisseur i
join match m on m.investisseur_ID = i.ID_investisseur
join statut_match s on s.ID_statut_match = m.statut_match_id
where "statut investisseur" !='relancer'
group by s.statut_match, i.nom
order by "Nombre" DESC;



SELECT 
    col_nom AS "Nom d'investisseur",
    col_statut AS "Statut investisseur", 
    col_nombre AS "Nombre"
FROM (
    SELECT 
        'TOTAL' AS col_nom,
        '' AS col_statut,
        (SELECT COUNT(*)
         FROM match m
         JOIN statut_match s ON s.ID_statut_match = m.statut_match_id
         WHERE s.statut_match != 'relancer') AS col_nombre,
        0 AS sort_order
    
    UNION ALL
    
    SELECT 
        i.nom AS col_nom,
        s.statut_match AS col_statut,
        COUNT(*) AS col_nombre,
        1 AS sort_order
    FROM investisseur i
    JOIN match m ON m.investisseur_ID = i.ID_investisseur
    JOIN statut_match s ON s.ID_statut_match = m.statut_match_id
    WHERE s.statut_match != 'relancer'
    GROUP BY i.nom, s.statut_match
) AS combined_data
ORDER BY 
    sort_order,
    CASE WHEN sort_order = 1 THEN col_nombre END DESC;
	
	
	
	
	
SELECT COUNT(*) AS col_nombre
         FROM match m
         JOIN statut_match s ON s.ID_statut_match = m.statut_match_id
         WHERE s.statut_match != 'relancer' 