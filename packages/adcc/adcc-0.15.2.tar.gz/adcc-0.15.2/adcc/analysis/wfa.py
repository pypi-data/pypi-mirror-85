

def compute_hole_density(tdm, ovlp):
    return tdm @ ovlp @ tdm.T


def compute_particle_density(tdm, ovlp):
    return tdm.T @ ovlp @ tdm
