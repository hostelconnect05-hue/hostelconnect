import { useState } from 'react';
import ContextActionModal from '../../components/ContextActionModal';
import { API_BASE_URL } from '../../utils/config';
import '../../styles/admin-room-utilities.css';

const WardenRoomUtilities = () => {
  const [verifying, setVerifying] = useState(false);
  const [recalculating, setRecalculating] = useState(false);
  const [verifyResult, setVerifyResult] = useState(null);
  const [recalculateResult, setRecalculateResult] = useState(null);
  const [showRecalculateConfirm, setShowRecalculateConfirm] = useState(false);
  const [feedbackModal, setFeedbackModal] = useState({ open: false, title: '', message: '', tone: 'primary' });

  const isBusy = verifying || recalculating;

  const openFeedbackModal = (title, message, tone = 'primary') => {
    setFeedbackModal({ open: true, title, message, tone });
  };

  const handleVerifyOccupancy = async () => {
    setVerifying(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/warden/rooms/verify-occupancy`);
      const data = await response.json();
      setVerifyResult(data);
    } catch (error) {
      console.error('Error verifying occupancy:', error);
      openFeedbackModal('Verification Failed', 'Failed to verify occupancy', 'danger');
    } finally {
      setVerifying(false);
    }
  };

  const handleRecalculateOccupancyClick = () => {
    setShowRecalculateConfirm(true);
  };

  const handleRecalculateOccupancyConfirm = async () => {
    setShowRecalculateConfirm(false);
    setRecalculating(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/warden/rooms/recalculate-occupancy`, {
        method: 'POST'
      });
      const data = await response.json();
      if (data.success) {
        setRecalculateResult(data);
        openFeedbackModal('Recalculation Complete', data.message, 'success');
        await handleVerifyOccupancy();
      } else {
        openFeedbackModal('Recalculation Failed', `Failed: ${data.message}`, 'danger');
      }
    } catch (error) {
      console.error('Error recalculating occupancy:', error);
      openFeedbackModal('Recalculation Failed', 'Failed to recalculate occupancy', 'danger');
    } finally {
      setRecalculating(false);
    }
  };

  return (
    <div className="room-utilities-container">
      <header className="utilities-header page-header-card">
        <div className="page-header-text">
          <h1>Room Utilities</h1>
          <p>Warden tools for room occupancy consistency</p>
        </div>
      </header>

      <div className="utilities-grid">
        <div className="utility-card">
          <div className="card-icon">🔍</div>
          <h2>Verify Occupancy</h2>
          <p>Check whether room occupancy counts match active student assignments</p>
          <button
            className="btn-primary"
            onClick={handleVerifyOccupancy}
            disabled={isBusy}
          >
            {verifying ? 'Verifying...' : 'Verify Now'}
          </button>

          {verifyResult && (
            <div className={`result-box ${verifyResult.has_issues ? 'warning' : 'success'}`}>
              {verifyResult.has_issues ? (
                <>
                  <h3>⚠️ Issues Found</h3>
                  <p>{verifyResult.discrepancies.length} rooms have incorrect occupancy counts</p>
                  <div className="discrepancies-list">
                    {verifyResult.discrepancies.map((disc, idx) => (
                      <div key={idx} className="discrepancy-item">
                        <strong>Room {disc.room_number}</strong> in {disc.block_name}
                        <br />
                        Stored: {disc.stored_count} | Actual: {disc.actual_count} | Capacity: {disc.capacity}
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <>
                  <h3>✅ All Clear</h3>
                  <p>All room occupancy counts are correct</p>
                </>
              )}
            </div>
          )}
        </div>

        <div className="utility-card">
          <div className="card-icon">🔄</div>
          <h2>Recalculate Occupancy</h2>
          <p>Recompute occupancy counts from actual room assignments</p>
          <button
            className="btn-warning"
            onClick={handleRecalculateOccupancyClick}
            disabled={isBusy}
          >
            {recalculating ? 'Processing...' : 'Recalculate All'}
          </button>

          {recalculateResult && (
            <div className="result-box success">
              <h3>✅ Done</h3>
              <p>{recalculateResult.message}</p>
            </div>
          )}
        </div>
      </div>

      <div className="info-section">
        <h3>💡 Warden Tips</h3>
        <ul>
          <li><strong>Verify Occupancy:</strong> Run before assigning rooms or reviewing room issues</li>
          <li><strong>Recalculate Occupancy:</strong> Use if occupancy appears stale or inconsistent</li>
          <li>Use both tools together to keep room data accurate</li>
        </ul>
      </div>

      <ContextActionModal
        open={showRecalculateConfirm}
        title="Recalculate Occupancy"
        message="This will recalculate occupancy counts for all rooms. Continue?"
        confirmText="Recalculate"
        cancelText="Cancel"
        tone="warning"
        onConfirm={handleRecalculateOccupancyConfirm}
        onClose={() => setShowRecalculateConfirm(false)}
      />

      <ContextActionModal
        open={feedbackModal.open}
        title={feedbackModal.title}
        message={feedbackModal.message}
        confirmText="OK"
        tone={feedbackModal.tone}
        hideCancel
        onConfirm={() => setFeedbackModal({ open: false, title: '', message: '', tone: 'primary' })}
        onClose={() => setFeedbackModal({ open: false, title: '', message: '', tone: 'primary' })}
      />
    </div>
  );
};

export default WardenRoomUtilities;
