import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import axios from 'axios';

const Groups = () => {
  const [groups, setGroups] = useState([]);
  const [keywords, setKeywords] = useState([]);
  const [newKeyword, setNewKeyword] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchGroups();
    fetchKeywords();
  }, []);

  const fetchGroups = async () => {
    try {
      const response = await axios.get('/api/facebook/groups');
      setGroups(response.data);
    } catch (error) {
      console.error('Error fetching groups:', error);
    }
  };

  const fetchKeywords = async () => {
    try {
      const response = await axios.get('/api/keywords');
      setKeywords(response.data);
    } catch (error) {
      console.error('Error fetching keywords:', error);
    }
  };

  const handleSearchGroups = async () => {
    try {
      const response = await axios.post('/api/facebook/search-groups', {
        keywords: keywords.map(k => k.word)
      });
      setGroups(response.data);
    } catch (error) {
      console.error('Error searching groups:', error);
    }
  };

  const handleAddKeyword = async () => {
    if (!newKeyword) return;
    try {
      await axios.post('/api/keywords', { word: newKeyword });
      setNewKeyword('');
      fetchKeywords();
    } catch (error) {
      console.error('Error adding keyword:', error);
    }
  };

  const handleDeleteKeyword = async (keywordId) => {
    try {
      await axios.delete(`/api/keywords/${keywordId}`);
      fetchKeywords();
    } catch (error) {
      console.error('Error deleting keyword:', error);
    }
  };

  const handleJoinGroup = async (groupId) => {
    try {
      await axios.post(`/api/facebook/join-group/${groupId}`);
      fetchGroups();
    } catch (error) {
      console.error('Error joining group:', error);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* מילות מפתח */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              מילות מפתח
            </Typography>
            <Box sx={{ display: 'flex', mb: 2 }}>
              <TextField
                fullWidth
                value={newKeyword}
                onChange={(e) => setNewKeyword(e.target.value)}
                placeholder="הוסף מילת מפתח חדשה"
              />
              <Button
                variant="contained"
                onClick={handleAddKeyword}
                startIcon={<AddIcon />}
                sx={{ ml: 1 }}
              >
                הוסף
              </Button>
            </Box>
            <List>
              {keywords.map((keyword) => (
                <ListItem key={keyword.id}>
                  <ListItemText primary={keyword.word} />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      onClick={() => handleDeleteKeyword(keyword.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* קבוצות */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              קבוצות
            </Typography>
            <Button
              fullWidth
              variant="contained"
              onClick={handleSearchGroups}
              sx={{ mb: 2 }}
            >
              חפש קבוצות חדשות
            </Button>
            <List>
              {groups.map((group) => (
                <ListItem key={group.id}>
                  <ListItemText
                    primary={group.name}
                    secondary={`סוג: ${group.privacy}`}
                  />
                  <ListItemSecondaryAction>
                    {!group.is_joined && (
                      <Button
                        variant="outlined"
                        onClick={() => handleJoinGroup(group.id)}
                      >
                        הצטרף
                      </Button>
                    )}
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Groups;
