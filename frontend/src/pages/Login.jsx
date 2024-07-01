
import React from 'react';
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';

const Login = () => {

    return (
        <div className="p-d-flex p-flex-column p-ai-center p-jc-center" style={{ height: '100vh', textAlign: 'center' }}>
            <Card title="What?!" subTitle="You are not logged in yet?!?" className="p-shadow-3">
                <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e358805f-3c84-4745-9628-f4f8eeca8d59/dh9ptp8-b662f772-dcec-493d-9fd1-6ff783626b2a.jpg/v1/fit/w_375,h_375,q_70,strp/tmnt__150_by_iancranium_dh9ptp8-375w.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTAyNCIsInBhdGgiOiJcL2ZcL2UzNTg4MDVmLTNjODQtNDc0NS05NjI4LWY0ZjhlZWNhOGQ1OVwvZGg5cHRwOC1iNjYyZjc3Mi1kY2VjLTQ5M2QtOWZkMS02ZmY3ODM2MjZiMmEuanBnIiwid2lkdGgiOiI8PTEwMjQifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.awtoNM6oZeECAJCMCvsI-Xi4hdm1keIyuNOJlDSKDOE"
                    alt="Funny placeholder" style={{ marginBottom: '1em', borderRadius: '50%' }} />
                <p style={{ fontSize: '1.2em' }}>You can only enter the VIP section with a ticket :-)</p>
                <Button label="Login with Spotify" icon="pi pi-spotify" className="p-button-rounded p-button-success p-mt-3" style={{ width: '70%' }}
                    onClick={() => window.location.href = "http://localhost:8000/api/auth/"} />
            </Card>
        </div>
    );
};

export default Login;

