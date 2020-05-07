import React from 'react';
import { Link } from 'react-router-dom';

import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles({
    root: {
        maxWidth: '500px',
        margin: '0 auto',
    },
    card: {
        minWidth: 275,
        margin: '2em 0',
    },
});

const docTree = new Map(Object.entries(DOC_TREE))
const comparer = (a, b) => {
    const reg = /(\d+)/
    const extractNum = str => parseInt(str.match(reg)[0], 10)
    return extractNum(a) - extractNum(b)
}
docTree.forEach(v => v.sort(comparer))

export default () => {
    const classes = useStyles(); // Hook must be inside
    return (
        <div className={classes.root}>
            {Array.from(docTree).map(([cat, subcatList]) => (
                <Card key={cat} variant='outlined' className={classes.card}>
                    <CardContent>
                        <Typography gutterBottom>{cat}</Typography>
                        {subcatList.map(subcat => (
                            <Button
                                key={`${cat}/${subcat}`}
                                component={Link}
                                to={`/${cat}/${subcat}`}
                                target='_blank'
                            > {subcat}</Button>
                        ))}
                    </CardContent>
                </Card>
            ))}
        </div>
    )
}