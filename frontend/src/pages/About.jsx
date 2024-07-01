import React from 'react';
import { Card } from 'primereact/card';
import { Avatar } from 'primereact/avatar';
import '../styles/About.css'
import Leonardo from '../assets/testimonials/leonardo.jpeg'
import Raphael from '../assets/testimonials/raphael.jpeg'
import Michelangello from '../assets/testimonials/michelangello.jpeg'
import Donatello from '../assets/testimonials/donatello.jpeg'

const About = () => {
  
  const testimonials = [
    { name: 'Leonardo', image: Leonardo, text: 'Meloturtle generates the best playlists to keep me sharp and focused during training!' },
    { name: 'Raphael', image: Raphael, text: 'The recommendations are as fresh as a New York slice! I love using it for special dinners.' },
    { name: 'Michelangelo', image: Michelangello, text: 'Cowabunga! Meloturtle rocks my world whenever im skating' },
    { name: 'Donatello', image: Donatello, text: 'Even a tech genius like me is impressed with Meloturtle!' },
  ];

  const team = [
    { name: 'David Olimpio', role: 'Creator', image: 'https://media.licdn.com/dms/image/D4D03AQHvF9W5A0ihuQ/profile-displayphoto-shrink_200_200/0/1693814703904?e=1724284800&v=beta&t=-lu5G6HWhMnj1I7gcep3TrgBX1_EvgwVIO4TUoGu5hw' },
    { name: 'Coffee', role: 'Co-creator and support director', image: 'https://live.staticflickr.com/4523/38669697181_0ca51a191f_b.jpg' },
  ];

  const renderTeamMember = (member) => (
    <div className="p-col-12 p-md-4" key={member.name}>
      <Card title={member.name} subTitle={member.role} className='team-item'>
        <Avatar image={member.image} shape="circle" size="xlarge" className="p-mb-2 p-avatar" />
      </Card>
    </div>
  );

  const renderTestimonial = (testimonial) => (
    <div key={testimonial.name}>
      <Card className="testimonial-item">
        <Avatar image={testimonial.image} shape="circle" size="xlarge" className="p-mb-2 p-avatar" />
        <h3>{testimonial.name}</h3>
        <p>"{testimonial.text}"</p>
      </Card>
    </div>
  );



  return (
    <div className="about-page">
      <div className="p-col-12 p-md-8">
        <Card title="Our Mission">
          <p>
            At Meloturtle, our mission is to revolutionize the way you discover and enjoy music.
            We provide personalized music recommendations tailored to your taste, helping you find your next favorite song or artist.
          </p>
        </Card>
      </div>

      <div className="p-col-12 p-md-8">
        <Card title="Features">
          <ul className='features'>
            <li>Personalized music recommendations with AI models</li>
            <li>Seamless integration with Spotify</li>
            <li>Curated playlists for every mood and occasion</li>
            <li>Discover new artists and genres</li>
          </ul>
        </Card>
      </div>

      <div className="people-wrapper">
        <div className="team-section">
          <Card title="Meet the Team">
            <div className="team-grid">
              {team.map(renderTeamMember)}
            </div>
          </Card>
        </div>

        <div className="testimonials-section">
          <Card title="Testimonials">
            <div className="testimonials-grid">
              {testimonials.map(renderTestimonial)}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default About;
