import React from 'react';
import { Box, Typography, Container, Paper, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import SecurityIcon from '@mui/icons-material/Security';

const LandingPage = () => {
  return (
    <Container maxWidth="md">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          py: 8,
        }}
      >
        {/* Logo and Title */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 2,
            mb: 6,
          }}
        >
          <SecurityIcon sx={{ fontSize: 60, color: '#1E40AF' }} />
          <Typography
            variant="h2"
            component="h1"
            sx={{
              fontWeight: 'bold',
              background: 'linear-gradient(45deg, #0A2472 0%, #1E3B8A 30%, #2B4ECB 60%, #4169E1 90%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              color: 'transparent',
            }}
          >
            SentinAI
          </Typography>
        </Box>

        {/* Description */}
        <Paper
          elevation={0}
          sx={{
            p: 4,
            mb: 6,
            maxWidth: '800px',
            backdropFilter: 'blur(8px)',
          }}
        >
          <Typography variant="h5" component="h2" gutterBottom align="center" sx={{ color: '#FFFFFF' }}>
            Advanced Multimodal Threat Detection System
          </Typography>
          <Typography variant="body1" paragraph align="center" sx={{ mb: 3, color: 'rgba(255, 255, 255, 0.8)' }}>
            SentinAI is a cutting-edge defense platform that combines sonar and camera data 
            with advanced AI to provide real-time threat analysis and automated agency notification. 
            Our system processes multiple data streams simultaneously to ensure maximum security 
            and rapid response capabilities.
          </Typography>
          <Typography variant="body1" align="center" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
            Powered by state-of-the-art LLM technology for precise threat assessment 
            and instantaneous multi-agency coordination.
          </Typography>
        </Paper>

        {/* Dashboard Link */}
        <Button
          component={Link}
          to="/dashboard"
          variant="contained"
          size="large"
          sx={{
            py: 2,
            px: 6,
            fontSize: '1.2rem',
          }}
        >
          Access Dashboard
        </Button>
      </Box>
    </Container>
  );
};

export default LandingPage;
