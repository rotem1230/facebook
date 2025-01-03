import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Button,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import axios from 'axios';

const Dashboard = () => {
  const [leads, setLeads] = useState([]);
  const [stats, setStats] = useState({
    totalLeads: 0,
    respondedLeads: 0,
    leadsByType: {}
  });

  useEffect(() => {
    fetchLeads();
    fetchStats();
  }, []);

  const fetchLeads = async () => {
    try {
      const response = await axios.get('/api/leads');
      setLeads(response.data);
    } catch (error) {
      console.error('Error fetching leads:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/leads/statistics');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    }
  };

  const columns = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'content', headerName: 'תוכן', width: 300 },
    { field: 'post_type', headerName: 'סוג', width: 130 },
    { field: 'responded', headerName: 'נענה', width: 130, type: 'boolean' },
    { field: 'created_at', headerName: 'תאריך יצירה', width: 180 },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* סטטיסטיקות */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              סטטיסטיקות
            </Typography>
            <Typography component="p" variant="h4">
              {stats.totalLeads} לידים
            </Typography>
            <Typography color="text.secondary" sx={{ flex: 1 }}>
              {stats.respondedLeads} נענו
            </Typography>
          </Paper>
        </Grid>

        {/* גרף */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              לידים לאורך זמן
            </Typography>
            <LineChart width={600} height={300} data={leads}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="created_at" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="id" stroke="#8884d8" />
            </LineChart>
          </Paper>
        </Grid>

        {/* טבלת לידים */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              לידים אחרונים
            </Typography>
            <div style={{ height: 400, width: '100%' }}>
              <DataGrid
                rows={leads}
                columns={columns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                checkboxSelection
                disableSelectionOnClick
              />
            </div>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
