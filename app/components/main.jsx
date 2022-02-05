import { Button } from '@mui/material';
import styles from '../styles/Main.module.css';
import { localIP } from './config';

//! You must set your local IP address below so that the
export default function Main() {
    async function sendCommand(command) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({app: command})
        };
        fetch('http://' + localIP + ':5000/api/app', requestOptions);
    }

    return (
        <div className={styles.container}>
            <Button
            className={styles.button}
                variant='outlined'
                onClick={() => sendCommand('clock')}
            >
                Clock
            </Button>
            <Button
            className={styles.button}
                variant='outlined'
                onClick={() => sendCommand('picture')}
            >
                Picture
            </Button>
            <Button
            className={styles.button}
                variant='outlined'
                onClick={() => sendCommand('ticker')}
            >
                Ticker
            </Button>
            <Button
            className={styles.button}
                variant='outlined'
                onClick={() => sendCommand('solid')}
            >
                Solid
            </Button>
            <Button
            className={styles.button}
                variant='outlined'
                onClick={() => sendCommand('clear')}
            >
                Clear
            </Button>
        </div>
    );
}
