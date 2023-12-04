import { Outlet, useNavigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { useEffect } from 'react';

const PrivateRoute = ({ auth }) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!auth.isAuthenticated) {
      navigate('/login');
    }
  }, [auth, navigate]);

  if (!auth.isAuthenticated) {
    return null;
  }

  return <Outlet />;
};

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps)(PrivateRoute);
