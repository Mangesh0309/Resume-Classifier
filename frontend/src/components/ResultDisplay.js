import React from 'react';
import { Box, Typography, Chip, Stack, Rating } from '@mui/material';
import WorkIcon from '@mui/icons-material/Work';
import StarIcon from '@mui/icons-material/Star';
import AssessmentIcon from '@mui/icons-material/Assessment';

function ResultDisplay({ result }) {
  const getCategoryColor = (category) => {
    switch (category.toLowerCase()) {
      case 'software_engineer':
        return '#2196f3';  // blue
      case 'data_scientist':
        return '#4caf50';  // green
      case 'product_manager':
        return '#f44336';  // red
      default:
        return '#757575';  // grey
    }
  };

  const getQualityColor = (quality) => {
    switch (quality.toLowerCase()) {
      case 'best':
        return '#4caf50';  // green
      case 'good':
        return '#2196f3';  // blue
      case 'average':
        return '#ff9800';  // orange
      case 'poor':
        return '#f44336';  // red
      default:
        return '#757575';  // grey
    }
  };

  const getQualityRating = (quality) => {
    switch (quality.toLowerCase()) {
      case 'best':
        return 5;
      case 'good':
        return 4;
      case 'average':
        return 3;
      case 'poor':
        return 2;
      default:
        return 1;
    }
  };

  return (
    <Box sx={{ mt: 4, textAlign: 'center' }}>
      <Typography variant="h6" gutterBottom>
        Classification Result
      </Typography>
      
      <Stack spacing={2} alignItems="center">
        <Chip
          icon={<WorkIcon />}
          label={result.category.replace('_', ' ').toUpperCase()}
          sx={{
            bgcolor: getCategoryColor(result.category),
            color: 'white',
            fontSize: '1.1rem',
            py: 2
          }}
        />
        
        <Box>
          <Typography variant="subtitle1" gutterBottom>
            Resume Quality
          </Typography>
          <Chip
            icon={<AssessmentIcon />}
            label={result.quality.toUpperCase()}
            sx={{
              bgcolor: getQualityColor(result.quality),
              color: 'white',
              fontSize: '1.1rem',
              py: 2
            }}
          />
          <Box sx={{ mt: 1 }}>
            <Rating
              value={getQualityRating(result.quality)}
              readOnly
              icon={<StarIcon fontSize="inherit" />}
              emptyIcon={<StarIcon fontSize="inherit" />}
              size="large"
            />
          </Box>
        </Box>
        
        <Typography variant="body2" color="textSecondary">
          File: {result.filename}
        </Typography>
      </Stack>
    </Box>
  );
}

export default ResultDisplay;
