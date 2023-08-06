import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from imblearn.metrics import specificity_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from scipy import interp

class MetricsVisualization:
    legend = {
        'd_load': ('Data Loading', 'maroon'),
        'd_transfer': ('Data Transfer', 'yellow'),
        'zero_grads': ('Zero Gradient', 'indigo'),
        'forward': ('Forward Pass', 'green'),
        'prediction': ('Prediction', 'blue'),
        'loss': ('Loss Computation', 'magenta'),
        'backward': ('Backward Pass', 'darkcyan'),
        'optimizer': ('Optimization Algorithm', 'darkslategray')
    }

    phases = ['train', 'val']

    metrics = ['loss',
               'overall_accuracy',
               'overall_cohen_kappa',
               'overall_recall',
               'overall_f1_score',
               'overall_precision',
               'overall_specificity']

    @staticmethod    
    def show_all(classification_analysis):
        # Show confusion metrics, confusion table, and classes metrics 
        for phase in MetricsVisualization.phases:
            phase_metrics = classification_analysis.get_last_epoch_metrics(phase)
            MetricsVisualization.phase_visualization(phase_metrics)

        # Show metric per epoch line plot
        for metric in MetricsVisualization.metrics:
            train_metrics = classification_analysis.get_epochs_metric(metric, MetricsVisualization.phases[0])
            val_metrics = classification_analysis.get_epochs_metric(metric, MetricsVisualization.phases[1])

            MetricsVisualization.line_plot(train_metrics, val_metrics, metric)
 
    @staticmethod
    def phase_visualization(phase_metrics):
        new_lines = '\n'
        
        print('Confusion Matrix' + new_lines)
        MetricsVisualization.show_confusion_matrix(phase_metrics)
        
        print(new_lines + 'Confusion Tables' + new_lines)
        MetricsVisualization.show_confusion_tables(phase_metrics)
        
        # Overall
        overall_metrics = {
            'Accuracy': phase_metrics.overall_accuracy,
            'Recall': phase_metrics.overall_recall,
            'Precision': phase_metrics.overall_precision,
            'F1_score': phase_metrics.overall_f1_score,
            'Specificity': phase_metrics.overall_specificity,
            'Cohen_Kappa': phase_metrics.overall_cohen_kappa
            }
        print(new_lines + 'Overall Metrics' + new_lines)
        MetricsVisualization.show_overall_metrics(overall_metrics)
        
        # Per class
        classes_metrics = {
            'Recall': phase_metrics.classes_recall,
            'Precision': phase_metrics.classes_precision,
            'F1_score': phase_metrics.classes_f1_score,
            'Specificity': phase_metrics.classes_specificity
            }
        print(new_lines + 'Classes Metrics' + new_lines)
        MetricsVisualization.show_classes_metrics(classes_metrics, phase_metrics.classes_labels)
        
        print(new_lines + 'ROC Curve' + new_lines)
        MetricsVisualization.show_roc_curve(phase_metrics.number_of_classes, phase_metrics.fpr, phase_metrics.tpr, phase_metrics.roc_auc)

    @staticmethod
    def show_confusion_matrix(classification_analysis):
        
        classification_analysis.calculate_confusion_matrix()
        # fig = plt.figure(figsize=(8,3))
        fig = plt.figure(figsize=(10,4))
        ax = plt.subplot(1,2,1)
        MetricsVisualization.plot_confusion_matrix(classification_analysis.confusion_matrix, 
                                                   classification_analysis.classes_labels,
                                                   title = 'Confusion Matrix',
                                                   cmap = plt.cm.Blues,
                                                   figure_axis = ax)
        
        ax = plt.subplot(1,2,2)
        MetricsVisualization.plot_confusion_matrix(classification_analysis.normalized_confusion_matrix, 
                                                   classification_analysis.classes_labels,
                                                   title = 'Normalized Confusion Matrix',
                                                   cmap = plt.cm.Blues,
                                                   figure_axis = ax)
        fig.tight_layout()
        plt.show()

    @staticmethod
    def show_confusion_tables(classification_analysis):
        classification_analysis.calculate_confusion_tables()
        fig = plt.figure(figsize=(8, classification_analysis.number_of_classes * 2))
        table_counter = 0
        for cls in range(classification_analysis.number_of_classes):
            table_counter += 1
            ax = plt.subplot(classification_analysis.number_of_classes, 3, table_counter)
            plt.grid(False)
            MetricsVisualization.plot_confusion_table_sample(ax)
            
            table_counter += 1
            ax = plt.subplot(classification_analysis.number_of_classes, 3, table_counter)
            MetricsVisualization.plot_confusion_matrix(classification_analysis.confusion_tables[cls], 
                                                       None,
                                                       title = classification_analysis.classes_labels[cls],
                                                       cmap = plt.cm.Blues,
                                                       figure_axis=ax)
            
            table_counter += 1
            ax = plt.subplot(classification_analysis.number_of_classes, 3, table_counter)
            MetricsVisualization.plot_confusion_matrix(classification_analysis.normalized_confusion_tables[cls], 
                                                       None,
                                                       title = classification_analysis.classes_labels[cls],
                                                       cmap = plt.cm.Blues,
                                                       figure_axis = ax)
        fig.tight_layout()
        plt.show()

    @staticmethod
    def plot_confusion_matrix(confusion_mat, classes, figure_axis, title=None, cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        """

        # Compute confusion matrix
        cm = confusion_mat

        ax = figure_axis
        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.grid(False)
        ax.figure.colorbar(im, ax=ax)

        if classes is not None:
            # We want to show all ticks...
            ax.set(xticks=np.arange(cm.shape[1]),
                   yticks=np.arange(cm.shape[0]),
                   # ... and label them with the respective list entries
                   xticklabels=classes, yticklabels=classes,
                   ylabel='True Label',
                   xlabel='Predicted Label')

            # Rotate the tick labels and set their alignment.
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        else:
            plt.setp( ax.get_xticklabels(), visible=False)
            plt.setp( ax.get_yticklabels(), visible=False)
            plt.setp( ax.get_xticklines(), visible=False)
            plt.setp( ax.get_yticklines(), visible=False)

        ax.set(title=title)

        # Loop over data dimensions and create text annotations.
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, cm[i, j],
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

    @staticmethod
    def plot_confusion_table_sample(figure_axis, cmap=plt.cm.Blues):
        cm = np.array([[1, 0.5],
                       [0.5, 1]])

        labels = [['TP', 'FP'],
                  ['FN', 'TN']]

        ax=figure_axis
        ax.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.grid(False)
        plt.setp( ax.get_xticklabels(), visible=False)
        plt.setp( ax.get_yticklabels(), visible=False)
        plt.setp( ax.get_xticklines(), visible=False)
        plt.setp( ax.get_yticklines(), visible=False)

        # Loop over data dimensions and create text annotations.
        thresh = cm.max() / 2.

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, labels[i][j],
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

    @staticmethod
    def line_plot(y_train, y_val, metric):

        print('\n')
        if metric == 'Loss':
            print('Training {} Min: {:0.3f} in epoch {}, Max: {:0.3f}, Current: {:0.3f}'.format(
                metric, min(y_train), np.array(y_train).argmin(), max(y_train), y_train[-1]))
            print('Validation {} Min: {:0.3f} in epoch {}, Max: {:0.3f}, Current: {:0.3f}'.format(
                metric, min(y_val), np.array(y_val).argmin(), max(y_val), y_val[-1]))

        else:
            print('Training {} Min: {:0.3f}, Max: {:0.3f} in epoch {}, Current: {:0.3f}'.format(
                  metric, min(y_train), max(y_train), np.array(y_train).argmax(), y_train[-1]))
            print('Validation {} Min: {:0.3f}, Max: {:0.3f} in epoch {}, Current: {:0.3f}'.format(
                  metric, min(y_val), max(y_val), np.array(y_val).argmax(), y_val[-1]))
        plt.figure(figsize=(9,5))
        plt.plot(y_train, label='Training')
        plt.plot(y_val, label='Validation')
        plt.xlabel('Epoch')
        plt.ylabel(metric)
        plt.ylim([0, max([1] + y_train + y_val)])
        plt.title(metric)
        plt.grid(True)
        plt.legend()
        plt.show()
        
    @staticmethod
    def steps_timing_visualization(steps_timing, not_included = []):
        total = list()
        average = list()
        colors = list()
        legends = list()
        valid_steps= dict()
        plt.figure(figsize=(8,6))
        plt.xlabel('Iteration number')
        plt.ylabel('Time [Sec]')
        plt.grid(True)

        for key in steps_timing:
            if key in not_included:
                continue
                
            if len(steps_timing[key]) > 0:
                total.append(sum(steps_timing[key]))
                average.append(sum(steps_timing[key]) / len(steps_timing[key]))
                colors.append(MetricsVisualization.legend[key][1])
                legends.append(MetricsVisualization.legend[key][0])
                valid_steps[key] = steps_timing[key]
                plt.plot(steps_timing[key], label=MetricsVisualization.legend[key][0], color=MetricsVisualization.legend[key][1])
        plt.legend() 
        plt.show()
        
        plt.figure(figsize=(8,6))
        plt.xlabel('phases')
        plt.ylabel('Total time [Sec]')
        plt.grid(True)
        y_values = np.arange(len(valid_steps))
        for i in range(len(total)):
            plt.bar(y_values[i], total[i], color = colors[i], label = legends[i])
        plt.xticks(y_values, valid_steps, rotation='vertical')
        plt.legend()
        plt.show()
        
        plt.figure(figsize=(8,6))
        plt.xlabel('phases')
        plt.ylabel('Average time per batch [Sec]')
        plt.grid(True)
        y_values = np.arange(len(valid_steps))
        for i in range(len(average)):
            plt.bar(y_values[i], average[i], color = colors[i], label = legends[i])
        plt.xticks(y_values, valid_steps, rotation='vertical')
        plt.legend()
        plt.show()
        
    @staticmethod
    def misclassification(model, dataset, to_display):
        y_pred = model['best_params']['epoch_data']['y_pred_validation']
        for i in range(to_display):
            imgage, class_label = dataset.validation_dataset.imgs[i]
            if class_label != y_pred[i]:
                img = Image.open(imgage)
                plt.figure(figsize=(10, 10))
                plt.imshow(img)
                plt.grid(False)
                plt.title('Actual : {} , Prediction : {} \n image : {}'.format(dataset.classes_names[class_label], 
                                                                               dataset.classes_names[y_pred[i]], 
                                                                               imgage)) 
    
    @staticmethod
    def show_overall_metrics(overall_metrics, required_metrics = ['Accuracy', 'Recall', 'Precision', 'F1_score', 'Specificity', 'Cohen_Kappa']):
              
        overall_metrics = pd.Series(
                {m: overall_metrics[m] for m in required_metrics
                                       if m in overall_metrics.keys()})
        
        # Show overall metrics
        fig = plt.figure(figsize=(10, 5))
        ax = plt.subplot(1,2,1)
        overall_metrics.plot.bar()
        plt.title('Overall Metrics')
        plt.grid(True)
        plt.ylim((0,1.5))
        
        ax = plt.subplot(1,2,2)
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText = overall_metrics.values.reshape((len(overall_metrics),1)), 
                     colLabels = ['Values'], 
                     rowLabels = overall_metrics.index,
                     loc = 'center',
                     colWidths = [0.2]
                    )
        table.scale(2, 2)
        table.set_fontsize(12)
        plt.show()
        
    @staticmethod
    def show_classes_metrics(classes_metrics, classes_labels, required_metrics = [ 'Recall', 'Precision', 'F1_score', 'Specificity', 'Cohen_Kappa']):
        
        classes_metrics = pd.DataFrame(
            {m: classes_metrics[m] for m in required_metrics
                                   if m in classes_metrics.keys()})
        classes_metrics.index = classes_labels
        
        # Data table
        ax = plt.subplot(1, 1, 1)
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText = classes_metrics.values, 
                     colLabels = classes_metrics.columns, 
                     rowLabels = classes_metrics.index,
                     loc = 'center',
                     colWidths = [0.2]*len(classes_metrics.columns))
        
        table.scale(2, 2)
        table.set_fontsize(15)
        plt.grid(True)
        plt.show()
        
        # Compare between metrics
        classes_metrics.plot.bar()
        plt.title('Metrics Comparison')
        plt.grid(True)
        plt.legend(loc=0)
        plt.ylim((0,1.5))
        plt.show()
        
        # Compare between classes
        classes_metrics.T.plot.bar()
        plt.title('Classes Comparison')
        plt.grid(True)
        plt.ylim((0,1.5))
        plt.show()
    
    @staticmethod
    def show_roc_curve(number_of_classes, fpr, tpr, roc_auc):
        # Plot all ROC curves
        plt.figure(figsize=(7, 5))
        
        lw = 2
        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        if number_of_classes == 2:
            plt.plot(fpr, tpr,
                 label = 'ROC curve (area = {0:0.2f})'
                 ''.format(roc_auc),
                 color = 'crimson', linestyle = ':', linewidth = 4)
        else:
            
            # Micro average ROC
            plt.plot(fpr["micro"], self.tpr["micro"],
                 label='micro-average ROC curve (area = {0:0.2f})'
                 ''.format(roc_auc["micro"]),
                 color='deeppink', linestyle=':', linewidth=4)
        
            # Macro average ROC
            plt.plot(fpr["macro"], tpr["macro"],
                 label='macro-average ROC curve (area = {0:0.2f})'
                 ''.format(roc_auc["macro"]),
                 color = 'navy', linestyle = ':', linewidth = 4)
        
            # Classes ROC
            for i in range(number_of_classes):
                plt.plot(fpr[i], tpr[i],  lw=lw,
                 label='ROC curve of ({0}) (area = {1:0.2f})'
                 ''.format(classes_labels[i], roc_auc[i]))

            
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves')
        plt.legend(loc="lower right")
        plt.show()
    
class MetricsClaculation:
    def __init__(self, y_true, y_pred, y_score , loss, number_of_classes, average_type = 'macro', digits_count_fp = 3,classes_labels = None):
        """ Initialization function
            y_true: list or numpy array (number of samples)
            y_pred: list or numpy array (number of samples)
            y_score: numpy array contains the actual outputs before decision (number of samples, number of classes)
            loss: value of loss
            average_type: determine how to calculate the overall metrics
            digits_count_fp: number of digits after the floating point
            classes_labels: list of classes labels
        """
        
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.y_score = np.array(y_score)
        self.loss = loss
        self.number_of_classes = number_of_classes
        self.y_true_one_hot = label_binarize(y_true, classes=list(range(self.number_of_classes)))
        
        self.number_of_samples = len(self.y_true)
        self.number_of_samples_per_class = [(self.y_true==c).sum() 
                                for c in range(self.number_of_classes)]
        
        self.classes_labels = ['Class ' + str(c) for c in range(self.number_of_classes)] \
                                if classes_labels is None \
                                else classes_labels
        
        self.digits_count_fp = digits_count_fp
        self.average_type = average_type

        # Initialize
        self.TP = None
        self.FP = None
        self.TN = None
        self.FN = None
        self.confusion_matrix = None
        self.normalized_confusion_matrix = None
        self.confusion_tables = None
        self.normalized_confusion_tables = None
        self.overall_accuracy = None
        self.overall_recall = None
        self.classes_recall = None
        self.overall_precision = None
        self.classes_precision = None
        self.overall_f1_score = None
        self.classes_f1_score = None
        self.overall_specificity = None
        self.classes_specificity = None
        self.overall_cohen_kappa = None
        self.fpr = None
        self.tpr = None
        self.thresholds = None
        self.roc_auc = None
                
        self.TP_TN_FP_FN()
        self.calculate_confusion_matrix()
        self.calculate_confusion_tables()
        self.accuracy()
        self.recall()
        self.precision()
        self.f1_score()
        self.specificity()
        self.cohen_kappa()
        self.calculate_roc_auc()
        
    def TP_TN_FP_FN(self):
        self.TP = np.zeros(self.number_of_classes)
        self.FP = np.zeros(self.number_of_classes)
        self.TN = np.zeros(self.number_of_classes)
        self.FN = np.zeros(self.number_of_classes)
        
        for cls in range(self.number_of_classes):
            # Calculate
            self.TP[cls] = (self.y_pred[self.y_true == cls] == cls).sum()
            self.FN[cls] = (self.y_pred[self.y_true == cls] != cls).sum()
            
            self.TN[cls] = (self.y_pred[self.y_true != cls] != cls).sum()
            self.FP[cls] = (self.y_pred[self.y_true != cls] == cls).sum()            
    
    def calculate_confusion_matrix(self):
        """ Function to calculate confusion matrix and weighted confusion matrix """
        self.confusion_matrix = confusion_matrix(self.y_true, self.y_pred)
        
        classes_weights = np.array(self.number_of_samples_per_class).reshape(
            self.number_of_classes, 1)
        
        self.normalized_confusion_matrix = (self.confusion_matrix/classes_weights).round(self.digits_count_fp)
    
    def calculate_confusion_tables(self):
        """ Function to calculate confusion table and weighted confusion table 
            for each class
        """
        self.confusion_tables = np.zeros((self.number_of_classes, 2, 2))
        self.normalized_confusion_tables = np.zeros((self.number_of_classes, 2, 2))
        
        for cls in range(self.number_of_classes):
            # Normal confusion table
            self.confusion_tables[cls, 0, 0] = self.TP[cls] # TP
            self.confusion_tables[cls, 0, 1] = self.FP[cls] # FP
            self.confusion_tables[cls, 1, 0] = self.FN[cls] # FN
            self.confusion_tables[cls, 1, 1] = self.TN[cls] # TN
            
            # Weighted confusion table
            table_weights = self.confusion_tables[cls].sum(axis=0).reshape(1, 2)
            self.normalized_confusion_tables[cls] = (self.confusion_tables[cls]/table_weights).round(self.digits_count_fp)
        
        # Convert the data type into int
        self.confusion_tables = self.confusion_tables.astype(int)
    
    def accuracy(self, sample_weight = None):
        """ Refer to sklearn for full doc"""
        if sample_weight is None:
            sample_weight  = np.ones(self.number_of_samples)
        self.overall_accuracy = accuracy_score(
            self.y_true, self.y_pred, sample_weight=sample_weight).round(self.digits_count_fp)
        
    def recall(self):
        """Recall is also known as Sensitivity and True Positive Rate"""
        self.overall_recall = recall_score(
            self.y_true, self.y_pred, average = self.average_type).round(self.digits_count_fp)
        self.classes_recall = recall_score(
            self.y_true, self.y_pred, average = None).round(self.digits_count_fp)
        
    def precision(self):
        """ Precision or Positive Predictive Value """
        self.overall_precision = precision_score(
            self.y_true, self.y_pred, average = self.average_type).round(self.digits_count_fp)
        self.classes_precision = precision_score(
            self.y_true, self.y_pred, average = None).round(self.digits_count_fp)
    
    def f1_score(self):
        """ f1_score is harmonic mean of recall and precision"""
        self.overall_f1_score = f1_score(
            self.y_true, self.y_pred, average = self.average_type).round(self.digits_count_fp)
        self.classes_f1_score = f1_score(
            self.y_true, self.y_pred, average = None).round(self.digits_count_fp)
    
    def specificity(self):
        """ Specificity is also known as True Negative Rate """
        self.overall_specificity = specificity_score(
            self.y_true, self.y_pred, average = self.average_type).round(self.digits_count_fp)
        self.classes_specificity = specificity_score(
            self.y_true, self.y_pred, average = None).round(self.digits_count_fp)
    
    def cohen_kappa(self):
        self.overall_cohen_kappa = cohen_kappa_score(self.y_true, self.y_pred).round(self.digits_count_fp)    
        
    def calculate_roc_auc(self):
        """ Refer to : https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
        """
        if self.number_of_classes == 2:
            self.fpr, self.tpr, self.thresholds = roc_curve(self.y_true, self.y_score[:,1])
            self.roc_auc = auc(self.fpr, self.tpr).round(self.digits_count_fp)
            
            # Rounding
            self.fpr = self.fpr.round(self.digits_count_fp)
            self.tpr = self.tpr.round(self.digits_count_fp)
            self.thresholds = self.thresholds.round(self.digits_count_fp)
            return 
        
        # Compute ROC curve and ROC area for each class
        self.fpr = dict()    # fpr: False positive rate
        self.tpr = dict()    # tpr: True positive rate
        self.roc_auc = dict()
        for i in range(self.number_of_classes):
            self.fpr[i], self.tpr[i], _ = roc_curve(
                self.y_true_one_hot[:, i], self.y_score[:, i])
            self.roc_auc[i] = auc(self.fpr[i] , self.tpr[i]).round(
                self.digits_count_fp).round(self.digits_count_fp)
            
            # Rounding
            self.fpr[i] = self.fpr[i].round(self.digits_count_fp)
            self.tpr[i] = self.tpr[i].round(self.digits_count_fp)


        # Compute micro-average ROC curve and ROC area
        self.fpr["micro"], self.tpr["micro"], _ = roc_curve(
            self.y_true_one_hot.ravel(), self.y_score.ravel())
        self.roc_auc["micro"] = auc(self.fpr["micro"], self.tpr["micro"]).round(self.digits_count_fp)
        
        # Rounding
        self.fpr["micro"] = self.fpr["micro"].round(self.digits_count_fp)
        self.tpr["micro"] = self.tpr["micro"].round(self.digits_count_fp)
        
        # Compute macro-average ROC curve and ROC area
        
        # First aggregate all false positive rates
        all_fpr = np.unique(np.concatenate([self.fpr[i] for i in range(self.number_of_classes)]))

        # Then interpolate all ROC curves at this points
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(self.number_of_classes):
            mean_tpr += interp(all_fpr, self.fpr[i], self.tpr[i])

        # Finally average it and compute AUC
        mean_tpr /= self.number_of_classes
        
        # Rounding
        self.fpr["macro"] = all_fpr.round(self.digits_count_fp)
        self.tpr["macro"] = mean_tpr.round(self.digits_count_fp)
        self.roc_auc["macro"] = auc(self.fpr["macro"], self.tpr["macro"]).round(self.digits_count_fp)

class ClassificationAnalysis:
    def __init__(self):
        self.epochs_train_metircs = list()
        self.epochs_val_metircs = list()

    def add_epoch_train_metircs(self, train_metrics):
        self.epochs_train_metircs.append(train_metrics)

    def add_epoch_val_metircs(self, val_metrics):
        self.epochs_val_metircs.append(val_metrics)

    def get_last_epoch_metrics(self, phase):
        return eval(f'self.epochs_{phase}_metircs[-1]')

    def get_epochs_metric(self, metric, phase):
        return [eval(f'epoch_metircs.{metric}') for epoch_metircs in eval(f'self.epochs_{phase}_metircs')]

