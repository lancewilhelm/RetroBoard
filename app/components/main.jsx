import { Button } from 'react-bootstrap';
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
                variant='outline-dark'
                onClick={() => sendCommand('clock')}
            >
                Clock
            </Button>
            <Button
            className={styles.button}
                variant='outline-dark'
                onClick={() => sendCommand('image')}
            >
                Image
            </Button>
        </div>
    );
}
