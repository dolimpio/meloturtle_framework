import React from 'react';
import { useNavigate } from 'react-router-dom';

import { Card } from 'primereact/card';
import { Button } from 'primereact/button';

const NoPage = () => {
  const navigate = useNavigate();
  return (
    <div className="p-d-flex p-jc-center p-ai-center p-flex-grow-1">
      <Card title="Oops! Page Not Found" style={{ textAlign: 'center' }}>
        <i className="pi pi-exclamation-triangle" style={{ fontSize: '3em', color: 'var(--red-500)' }}></i>
        <h1>404</h1>
        <p>Looks like you took a wrong turn. But don't worry, we won't tell anyone!</p>
        <Button label="Go Home" icon="pi pi-home" onClick={() =>navigate('/')} />
      </Card>
    </div>
  );
}

export default NoPage;
