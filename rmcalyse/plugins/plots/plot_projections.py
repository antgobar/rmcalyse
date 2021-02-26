import matplotlib.pyplot as plt
import seaborn as sns

def plot_projections(x, y, weighting=None, show_points=False):


	sns.kdeplot(x=x, y=y, fill=True, weights=weighting, label='kde')
	
	if show_points == True:
		plt.scatter(x, y, label='data', c='darkorange', alpha=0.7)

	plt.legend()
	plt.gca().set_aspect('equal', adjustable='box')

	plt.show()
