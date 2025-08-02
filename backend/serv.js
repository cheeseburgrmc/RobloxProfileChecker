const express = require('express');
const app = express();
const axios = require('axios');
const path = require('path');

const PORT = process.env.PORT || 8080;

// Serve frontend
app.use(express.static(path.join(__dirname, '../public')));

// Home route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Convert username to user ID
app.get('/api/userid', async (req, res) => {
  const username = req.query.username;
  if (!username) return res.status(400).json({ error: 'Missing username' });

  try {
    const response = await axios.post(
      'https://users.roblox.com/v1/usernames/users',
      { usernames: [username] },
      { headers: { 'Content-Type': 'application/json' } }
    );

    if (response.data && response.data.data && response.data.data.length > 0) {
      res.json({ userId: response.data.data[0].id });
    } else {
      res.status(404).json({ error: 'User not found' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Roblox API failed', details: error.message });
  }
});

// Get groups from user ID
app.get('/api/groups', async (req, res) => {
  const userId = req.query.userid;
  if (!userId) return res.status(400).json({ error: 'Missing user ID' });

  try {
    const response = await axios.get(
      `https://groups.roblox.com/v1/users/${userId}/groups/roles`
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get group data', details: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
