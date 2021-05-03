import Head from 'next/head';
import styles from '../styles/Index.module.css';
import Main from '../components/main';

export default function Home() {
    return (
        <div className={styles.container}>
            <Head>
                <title>Retro Magic Board</title>
            </Head>
            <div className={styles.titleBar}>
                <h1 className={styles.title}>Magic Color Board</h1>
                <div className={styles.subtitle}>A board of wonders</div>
            </div>
            <Main />
        </div>
    );
}
