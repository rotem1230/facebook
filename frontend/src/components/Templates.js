import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import axios from 'axios';

const Templates = () => {
  const [templates, setTemplates] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentTemplate, setCurrentTemplate] = useState({
    name: '',
    content: '',
    type: ''
  });
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await axios.get('/api/templates');
      setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  const handleOpenDialog = (template = null) => {
    if (template) {
      setCurrentTemplate(template);
      setIsEditing(true);
    } else {
      setCurrentTemplate({ name: '', content: '', type: '' });
      setIsEditing(false);
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setCurrentTemplate({ name: '', content: '', type: '' });
    setIsEditing(false);
  };

  const handleSaveTemplate = async () => {
    try {
      if (isEditing) {
        await axios.put(`/api/templates/${currentTemplate.id}`, currentTemplate);
      } else {
        await axios.post('/api/templates', currentTemplate);
      }
      handleCloseDialog();
      fetchTemplates();
    } catch (error) {
      console.error('Error saving template:', error);
    }
  };

  const handleDeleteTemplate = async (templateId) => {
    try {
      await axios.delete(`/api/templates/${templateId}`);
      fetchTemplates();
    } catch (error) {
      console.error('Error deleting template:', error);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Typography component="h2" variant="h6" color="primary">
                תבניות תגובה
              </Typography>
              <Button
                variant="contained"
                onClick={() => handleOpenDialog()}
              >
                צור תבנית חדשה
              </Button>
            </Box>
            <List>
              {templates.map((template) => (
                <ListItem key={template.id}>
                  <ListItemText
                    primary={template.name}
                    secondary={`סוג: ${template.type}`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      onClick={() => handleOpenDialog(template)}
                      sx={{ mr: 1 }}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      edge="end"
                      onClick={() => handleDeleteTemplate(template.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* דיאלוג עריכה/יצירה */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {isEditing ? 'ערוך תבנית' : 'צור תבנית חדשה'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="שם התבנית"
              value={currentTemplate.name}
              onChange={(e) => setCurrentTemplate({
                ...currentTemplate,
                name: e.target.value
              })}
              fullWidth
            />
            <FormControl fullWidth>
              <InputLabel>סוג</InputLabel>
              <Select
                value={currentTemplate.type}
                onChange={(e) => setCurrentTemplate({
                  ...currentTemplate,
                  type: e.target.value
                })}
              >
                <MenuItem value="request">בקשה</MenuItem>
                <MenuItem value="complaint">תלונה</MenuItem>
                <MenuItem value="job_offer">הצעת עבודה</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="תוכן"
              value={currentTemplate.content}
              onChange={(e) => setCurrentTemplate({
                ...currentTemplate,
                content: e.target.value
              })}
              multiline
              rows={4}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>ביטול</Button>
          <Button onClick={handleSaveTemplate} variant="contained">
            שמור
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Templates;
