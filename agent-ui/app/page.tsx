'use client';

import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { encodePassphrase, generateRoomId, randomString } from '@/lib/client-utils';
import styles from '../styles/Home.module.css';

function StartMeeting() {
  const router = useRouter();
  const [e2ee, setE2ee] = useState(false);
  const [sharedPassphrase, setSharedPassphrase] = useState(randomString(64));

  const startMeeting = () => {
    if (e2ee) {
      router.push(`/rooms/${generateRoomId()}#${encodePassphrase(sharedPassphrase)}`);
    } else {
      router.push(`/rooms/${generateRoomId()}`);
    }
  };

  return (
    <div className={styles.tabContent}>
      <button style={{ marginTop: '1rem' }} className="lk-button" onClick={startMeeting}>
        Start Meeting
      </button>
    </div>
  );
}

export default function Page() {
  return (
    <>
      <main
        className={styles.main}
        data-lk-theme="default"
        style={{
          backgroundImage: "url('/images/background.jpg')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          minHeight: '100vh',
        }}
      >
        <div
  className="header"
  style={{
    backgroundColor: 'black',
    color: 'white',
    padding: '20px',
    borderRadius: '10px',
  }}
>
  <img src="/images/news.png" alt="NewsCaster AI" width="360" height="100" />
  <h2>
    <strong>NewsCaster AI</strong> – An open-source AI news avatar platform built with{' '}
    <a
      href="https://github.com/livekit/components-js?ref=meet"
      rel="noopener"
      style={{ color: 'lightblue' }}
    >
      LiveKit&nbsp;Components
    </a>
    ,{' '}
    <a
      href="https://livekit.io/cloud?ref=meet"
      rel="noopener"
      style={{ color: 'lightblue' }}
    >
      LiveKit&nbsp;Cloud
    </a>{' '}
    and Next.js, delivering video-based news and updates in real time.
  </h2>
</div>
        <StartMeeting />
      </main>

      <footer data-lk-theme="default">
        Hosted on{' '}
        <a href="https://livekit.io/cloud?ref=meet" rel="noopener">
          LiveKit Cloud
        </a>
        . Source code on{' '}
        <a href="https://github.com/livekit/meet?ref=meet" rel="noopener">
          GitHub
        </a>
        .
      </footer>
    </>
  );
}
